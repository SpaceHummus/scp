# Class for handeling switches / transistors 

import logging
import RPi.GPIO as GPIO


SWITCH_LED_PIN=23
SWITCH_AIR_SENSE_PIN=22
SWITCH_MEDTRONIC_PIN=13
SWITCH_ON = "on"
SWITCH_OFF = "off"

class SwitchHandler:

    def __init__(self):
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(SWITCH_LED_PIN, GPIO.OUT)
        GPIO.setup(SWITCH_AIR_SENSE_PIN, GPIO.OUT)
        GPIO.setup(SWITCH_MEDTRONIC_PIN, GPIO.OUT)

    # set the switch on or off     
    # switch:  SWITCH_LED_PIN / SWITCH_AIR_SENSE_PIN / SWITCH_MEDTRONIC_PIN
    # value: SWITCH_ON or SWITCH_OFF
    def set_switch(self,switch,value):
        # Notice: on = low, off = high
        if value == "on":
            logging.info("setting switch %d on",switch)
            GPIO.output(switch,False)
        else:
            logging.info("setting switch %d off",switch)
            GPIO.output(switch,True)