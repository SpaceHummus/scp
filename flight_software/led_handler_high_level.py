# This is a higher level of LED handler that controls switches as well as logic states

import switch_handler
import led_handler
from telematry_handler import TelematryHandler
import logging
import time
import system_state

current_logic_state = "Off"
sw_handler = switch_handler.SwitchHandler()

# This is the main function that sets the state. Each state is defined in logic_states.yaml in system_states
# If current state is identical to old one, we skip
# Input: new_logic_state can be a system_states dict or "off" to turn off all LEDs
def set_led_state(new_logic_state):
    global current_logic_state
    global sw_handler

    # Figure out current and new logic state's name
    if type(current_logic_state) is not str:
        current_logic_state_name = current_logic_state.name
    else:
        current_logic_state_name = current_logic_state
    if type(new_logic_state) is not str:
        new_logic_state_name = new_logic_state.name
    else:
        new_logic_state_name = new_logic_state
        
    # If current and new logic states are the same, skip, there is nothing to do.
    if current_logic_state_name == new_logic_state_name:
        return
        
    # Specify Transition Logic State
    ls_name = current_logic_state_name + "->" + new_logic_state_name + "_TransitionStep"
    
    # Before switching states, capture current telemetry status
    th = TelematryHandler()
    th.set_current_logic_state_name(ls_name+"0")
    th.write_telemetry_csv()
        
    # Entering a new state
    logging.info('Entering a new LED state:%s',new_logic_state_name) 
    
    # If current state is not off, power down LEDs first
    if current_logic_state_name.lower() != "off":
        logging.info('Powering down LEDs')
        
        # First step is to switch off FR LEDs
        th.set_current_logic_state_name(ls_name+"1")
        led_handler.light_far_red(0)
        time.sleep(0.5)
        th.write_telemetry_csv() # Gather paramters without FR
        
        # Next switch off all Neopixels
        th.set_current_logic_state_name(ls_name+"2")
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN,"off")
        time.sleep(0.5)
        th.write_telemetry_csv() # Gather paramters
    
    # If new state is not off, power up LEDs
    if new_logic_state_name.lower() != "off":
        logging.info('Powering up LEDs')
        
        # First, switch master power switch on
        th.set_current_logic_state_name(ls_name+"3")
        sw_handler.set_switch(switch_handler.SWITCH_LED_PIN,"on")
        time.sleep(1)
        th.write_telemetry_csv() # Gather paramters after switch is on
        
        # Next switch on FR LEDs
        th.set_current_logic_state_name(ls_name+"4")
        led_handler.light_far_red(new_logic_state.illumination.far_red)
        time.sleep(0.5)
        th.write_telemetry_csv() # Gather paramters of just FR
        
        # Finally Set Neopixel Values
        th.set_current_logic_state_name(ls_name+"5")
        if ( # Make sure at least one LED value is >0, if not there is no reason to send command
            new_logic_state.illumination.group1_rgb.R >= 0 or 
            new_logic_state.illumination.group1_rgb.G >= 0 or 
            new_logic_state.illumination.group1_rgb.B >= 0 or 
            new_logic_state.illumination.group2_rgb.R >= 0 or 
            new_logic_state.illumination.group2_rgb.G >= 0 or 
            new_logic_state.illumination.group2_rgb.B >= 0
            ):
            led_handler.light_all_pixels(
                new_logic_state.illumination.group1_rgb,
                new_logic_state.illumination.group2_rgb)
            time.sleep(0.5)
        else:
            logging.info('All neopixel values are 0, no reason to send a command to turn them on')
        th.write_telemetry_csv() # Gather paramters of just FR
        
    # Set new state
    current_logic_state = new_logic_state

# Set LEDs using rgb instead of state
def set_led_rgb(r1,g1,b1,r2,g2,b2,far_red):
    
    # Define dummy state
    rgb1 = system_state.RGB(r1,g1,b1)
    rgb2 = system_state.RGB(r2,g2,b2)
    camera_config = system_state.CameraConfiguration(60,60,10,[])
    ilumination = system_state.Illumination(rgb1,rgb2,far_red)
    state = system_state.SystemState(camera_config,ilumination,'my_state')
    
    # Make sure we switch to the new state
    current_logic_state = "Off"
    
    set_led_state(state)
    

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("scp_main.log"),
            logging.StreamHandler()
        ]
    )   

if __name__ == "__main__":
    setup_logging()
    th = TelematryHandler()
    th.start_telemetry_csv_file()

    # Define states and toggle between them
    rgb_day = system_state.RGB(150,210,210)
    rgb_night = system_state.RGB(0,0,0)
    camera_config = system_state.CameraConfiguration(60,60,10,[])
    day_ilumination = system_state.Illumination(rgb_day,rgb_day,12)
    night_ilumination = system_state.Illumination(rgb_night,rgb_night,0)
    day_in_group_1_ilumination = system_state.Illumination(rgb_day,rgb_night,12)
    
    # Add all states to a list
    states = list()
    states.append(system_state.SystemState(camera_config,day_ilumination,'day_all'))
    states.append(system_state.SystemState(camera_config,night_ilumination,'night_all'))
    states.append(system_state.SystemState(camera_config,day_in_group_1_ilumination,'day_in_group1'))
    
    # Go over all states in a cycle
    while(True):
        set_led_state(states[0]);
        time.sleep(5)
        set_led_state(states[0]);
        time.sleep(5)
        set_led_state(states[1]);
        time.sleep(5)
        set_led_state(states[2]);
        time.sleep(5)
        set_led_state("Off");
        time.sleep(5)
    

