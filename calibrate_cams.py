# Read yaml configurtation files, based on the schedule, setup lesds, take pictures

import time
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
from system_state import SystemState 
from system_state import CameraConfiguration
import logging
from camera_handler import CameraHandler
from gdrive_handler import GDriveHandler
import socket


# holds system states configurations
system_states={}
states_over_time=[]

# wait until DNS service is ready, otherwise GDrive access will not work. This is needed when we run on boot and DNS service tkaes time to load
def wait_4_dns():
    while (True):
        try:
            addr = socket.gethostbyname('www.googleapis.com')
            logging.info("Found DNS for www.googleapis.com. IP:%s",addr)
            return
        except:
            logging.error("DNS not ready yet...")
            time.sleep(1)
    


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
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )    

# read all system states from yaml file and load into memory
def get_system_states():
    file = open(r'logic_states.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    
    raw_system_states = conf_dic["system_states"]

    for i in range(len(raw_system_states)):
        name = raw_system_states[i]["name"]
        cam_conf=raw_system_states[i]["camera_configuration"]
        if cam_conf==None:
            state = SystemState(None,name)  
        else:
            image_frequency_min = cam_conf["image_frequency_min"]
            focus_position = cam_conf["focus_position"]
            exposure = cam_conf["exposure"]
            iso =cam_conf["ISO"]
            state = SystemState(CameraConfiguration(image_frequency_min,exposure,iso,focus_position),name)  
        state.print_values()
        system_states[name]=state
         

def get_state_over_time():
    global states_over_time
    file = open(r'logic_states.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    states_over_time = conf_dic["states_over_time"] 
    logging.info("states_over_time:%s",str(states_over_time))
    # print(time.mktime(datetime.strptime(d, "%Y/%m/%d %H:%M:%S").timetuple()))


def getGDrive_folder_id():
    # get G-Drive folder ID
    file = open(r'configuration.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    folder_id=conf_dic["folder_id"]
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
    full_path_file_name,title_name = camera.take_pic(get_file_name())
    
    try:
        g_drive.upload_file(full_path_file_name,title_name)
    except:
        logging.error("timeout while uploading file to G Drive")



def main():
    setup_logging()
    logging.info('*** Start ***')
    camera = CameraHandler('A',focus=150)
    camera.change_active_camera("C")
    camera.change_focus(150)



    for i in range(20):
        camera.change_active_camera("A")
        full_path_file_name,title_name = camera.take_pic(str(i))
        # return
        time.sleep(0.1)
        camera.change_active_camera("C")
        full_path_file_name,title_name = camera.take_pic(str(i))
        for s in range(5,0,-1):
            logging.info('count down %d:...',s)
            time.sleep(1)


if __name__ == "__main__":
    main()
