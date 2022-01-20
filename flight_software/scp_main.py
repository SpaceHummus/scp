# Read yaml configurtation files, based on the schedule, setup lesds, take pictures

import sys
sys.path.insert(1, '../common')
import time
import yaml
from datetime import datetime
import logging
import socket
import subprocess
import traceback
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from system_state import SystemState 
from system_state import CameraConfiguration
from system_state import Illumination
from system_state import RGB
from camera_handler import CameraHandler
from camera_handler_high_level import CameraHandlerHighLevel
from root_image_handler import RootImageHandler
from gdrive_handler import GDriveHandler
from telematry_handler import TelematryHandler
from utils import wait_4_dns
import switch_handler
import image_handler
import led_handler_high_level


CONF_FILE_NAME = "scp_conf.yaml"
WAIT_FOR_DNS_IN_SEC = 15
# holds system states configurations
system_states={}
states_over_time=[]
sw_handler = switch_handler.SwitchHandler()
medtronic_switch = "on"


# wait until DNS service is ready, otherwise GDrive access will not work. This is needed when we run on boot and DNS service tkaes time to load
# returns True if we got internet connection & DNS is working. otherwise False
# def wait_4_dns(max_retires):
#     t = time.time()
#     while (True):
#         try:
#             addr = socket.gethostbyname('www.googleapisAAA.com')
#             logging.info("Found DNS for www.googleapis.com. IP:%s",addr)
#             return True
#         except:
#             logging.error("DNS not ready yet...")
#             time.sleep(1)
#         if time.time()-t >= max_retires:
#             return False
    


# get the system's current state based on current time
def get_current_state():
    current_time = time.time()
    current_state="NA"
    # go over all states and find the one we sould use now
    for state in reversed(states_over_time):
        the_date = time.mktime(datetime.strptime(state[0], "%Y/%m/%d %H:%M:%S").timetuple())
        logging.debug("current time:%d the_date:%d",current_time , the_date)
        if current_time > the_date:
            current_state = state[1]
            break
    if current_state=="NA":
        logging.info("cant find states over time, taking first state")
        current_state = state[1]
            
    logging.info("current state found:%s",current_state)
    return system_states[current_state]

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("scp_main.log"),
            logging.StreamHandler()
        ]
    )   

# turn on/off the switches
def set_switches():
    global medtronic_switch
    file = open(r'configuration.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    sw_handler.set_switch(switch_handler.SWITCH_LED_PIN,switch_handler.SWITCH_ON)

    air_sense_switch = conf_dic["air_sense_switch_status"]
    logging.info("air_sense_switch:%s",air_sense_switch)
    sw_handler.set_switch(switch_handler.SWITCH_AIR_SENSE_PIN,air_sense_switch)

    medtronic_switch = conf_dic["medtronic_switch_status"]
    logging.info("medtronic_switch:%s",medtronic_switch)
    sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN,medtronic_switch)
    

# read all system states from yaml file and load into memory
def get_system_states():
    file = open(r'logic_states.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    file.close()
    
    raw_system_states = conf_dic["system_states"]
    for i in range(len(raw_system_states)):
        name = raw_system_states[i]["name"]
        cam_conf=raw_system_states[i]["camera_configuration"]
        illum=raw_system_states[i]["illumination"] 
        g1= illum["group1"]
        R1=g1["red"]
        G1=g1["green"]
        B1=g1["blue"]
        g2= illum["group2"]
        R2=g2["red"]
        G2=g2["green"]
        B2=g2["blue"]
        far_red= illum["far_red"]
        if cam_conf==None:
            cam_configuration = None  
        else:
            root_image_frequency_min = cam_conf["root_image_frequency_min"]
            image_frequency_min = cam_conf["image_frequency_min"]
            focus_position = cam_conf["focus_position"]
            cam_configuration = CameraConfiguration(image_frequency_min, root_image_frequency_min, focus_position)
        Illumination_group=Illumination(RGB(R1,G1,B1),RGB(R2,G2,B2),far_red)
        state = SystemState(cam_configuration,Illumination_group,name)  
        state.print_values()
        system_states[name]=state
         

def get_state_over_time():
    global states_over_time
    file = open(r'logic_states.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    states_over_time = conf_dic["states_over_time"] 
    file.close()
    logging.info("states_over_time:%s",str(states_over_time))
    # print(time.mktime(datetime.strptime(d, "%Y/%m/%d %H:%M:%S").timetuple()))


def getGDrive_folder_id():
    # get G-Drive folder ID
    file = open(CONF_FILE_NAME,"r")
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    folder_id=conf_dic["folder_id"]
    file.close()
    logging.info("G-Drive folder ID:%s",folder_id)
    return folder_id

# get configuration data from yaml file
def get_states_settings():
    get_system_states()
    get_state_over_time()
    
# get file name by date
def get_file_name ():
    now = datetime.now()
    return now.strftime("%y-%m-%d__%H_%M")

def take_pic_and_upload(camera,g_drive,focus):
    camera.change_focus(focus)
    full_path_file_name,title_name = camera.take_pic(get_file_name(),True)
    g_drive.upload_image(full_path_file_name,title_name)

# gets a list of files to upload to g-drive        
def upload_files(files, g_drive):
    for f in files:
        g_drive.upload_image(f[0],f[1])

# take pictures in all focus values
# returns a list of all file names that were taken
def take_pic_all_focus(camera,cameraID,focus_list,file_name_prefix):
    files_list=[]
    camera.change_active_camera(cameraID)
    for f in focus_list[cameraID]:
        camera.change_focus(f)
        full_path_file_name,title_name = camera.take_pic(file_name_prefix,True)
        image_handler.check_image(full_path_file_name)
        files_list.append((full_path_file_name,title_name))
    return files_list

def get_version():
    cmd ="git describe --tags"
    p = subprocess.Popen(cmd.split(),
                     stdout=subprocess.PIPE)
    ret, _ = p.communicate()
    return ret.strip()



def main():
    # Load up logging, gather first telemetry
    setup_logging()
    logging.info('*** Start *** ver %s',get_version())
    telematry_handler = TelematryHandler()
    telematry_handler.start_telemetry_csv_file() # Start a file by placing header if we haven't done so already
    telematry_handler.set_current_logic_state_name("Booting")
    telematry_handler.write_telemetry_csv() 
    
    # Get handler to G-Drive
    has_dns = wait_4_dns(WAIT_FOR_DNS_IN_SEC) # wait for DNS / Internet access
    if has_dns:
        g_drive_handler = GDriveHandler(getGDrive_folder_id())
        g_drive_handler.get_logic_sates_file()
        g_drive_handler.get_configuration_file()
    get_states_settings()

    # turn on/off the switches
    set_switches()

    # get handler for the cameras
    camera = CameraHandler()
    camera_handler_high_level = CameraHandlerHighLevel()
    root_image = RootImageHandler()
    last_pic_time = 0
    last_root_pic_time = 0
    while(True):
        # Record current time such that all steps in this iteration have the same time
        current_time = time.time()
    
        # Capture current logic state
        state = get_current_state()
        telematry_handler.set_current_logic_state_name(state.name)
        
        # Set LED status (internal logic will make sure we don't turn on/off leds if not needed)
        led_handler_high_level.set_led_state(state)

        # Take main pictures if needed
        enabled_cameras = camera_handler_high_level.get_enabled_cameras()
        file_list = []
        if (state.camera_configuration != None) and (current_time - last_pic_time >=(60*state.camera_configuration.image_frequency_min)):
            file_name_prefix = get_file_name() # File name prefix (date and time) is selected once before taking all images such that they have the same time
            for cam in enabled_cameras:
                file_list.extend(take_pic_all_focus(camera,cam,state.camera_configuration.focus_position,file_name_prefix))
                last_pic_time = time.time()
            logging.info("going to wait %d minute(s) before next picture",state.camera_configuration.image_frequency_min)
        
        # Take root pictures if needed
        if (medtronic_switch =="on") and (state.camera_configuration != None) and (current_time - last_root_pic_time >=(60*state.camera_configuration.root_image_frequency_min)):
        
            # Before turning on medtronic, switch off main LEDs
            led_handler_high_level.set_led_state("Off")
            
            # Reset the medtroic card
            sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN,switch_handler.SWITCH_OFF)
            sw_handler.set_switch(switch_handler.SWITCH_MEDTRONIC_PIN,switch_handler.SWITCH_ON)
            time.sleep(1) # wait for root psb to start...
            
            # Take the image
            root_image.take_pic(get_file_name())
            
            # Set LEDs back
            led_handler_high_level.set_led_state(state)
            
            # Set a handle for the next image
            last_root_pic_time = time.time()
            logging.info("going to wait %d minute(s) before next root picture",state.camera_configuration.root_image_frequency_min)
        
        telematry_handler.write_telemetry_csv() 
        logging.info('going to sleep a minute...')
        time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
        logging.error(traceback.format_exc())
    