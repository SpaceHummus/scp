# Read yaml configurtation files, based on the schedule, setup lesds, take pictures

import time
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
from system_state import SystemState 
from system_state import CameraConfiguration
from system_state import FocusPosition
import logging
from camera_handler import CameraHandler
from gdrive_handler import GDriveHandler

# holds system states configurations
system_states={}
states_over_time=[]

# get the system's current state based on current time
def get_current_state():
    current_time = time.time()
    for i in range(len(states_over_time)):
        d = time.mktime(datetime.strptime(states_over_time[i][0], "%Y/%m/%d %H:%M:%S").timetuple())
        if d>current_time:
            if i==0:
                logging.error("states_over_time starts after current time, taking first value")
                return states_over_time[i-1][1]
            else:
                return states_over_time[i-1][1]

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
            state = SystemState(CameraConfiguration(-1,-1,-1,FocusPosition(-1,-1,-1)),name)  
        else:
            image_frequency_min = cam_conf["image_frequency_min"]
            min_f = cam_conf["focus_position"]["min"]
            max_f = cam_conf["focus_position"]["max"]
            step_f = cam_conf["focus_position"]["step"]
            exposure = cam_conf["exposure"]
            iso =cam_conf["ISO"]
            state = SystemState(CameraConfiguration(image_frequency_min,exposure,iso,FocusPosition(min_f,max_f,step_f)),name)  
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
def get_settings():
    get_system_states()
    get_state_over_time()
    
# get file name by date
def get_file_name ():
    now = datetime.now()
    return now.strftime("%y-%m-%d__%H_%M")

def take_pic_and_upload(camera,g_drive,focus):
    camera.change_focus(focus)
    full_path_file_name,title_name = camera.take_pic(get_file_name())
    g_drive.upload_file(full_path_file_name,title_name)


def main():
    setup_logging()
    logging.info('*** Start ***')
    # get_settings()

    g_drive_handler = GDriveHandler(getGDrive_folder_id())
    camera = CameraHandler('A',focus=512)

    while(True):
        # take take pictures from camera A
        camera.change_active_camera("A")
        take_pic_and_upload(camera,g_drive_handler,512)
        take_pic_and_upload(camera,g_drive_handler,260)
        

        # take take pictures from camera C
        camera.change_active_camera("C")
        take_pic_and_upload(camera,g_drive_handler,512)
        take_pic_and_upload(camera,g_drive_handler,260)
    
        logging.info('going to sleep...')
        time.sleep(60*10)

    # while (True):
    #     get_current_state()
    #     time.sleep(1)

    # start_LED ()
    # for f in range(100,101,1):
    #     take_pic(0,False,f,5,5)
    #     take_pic (1,True,f,10,10)
    # stop_LED()
    logging.info('*** End ***')


if __name__ == "__main__":
    main()
