# Read yaml configurtation files, based on the schedule, setup lesds, take pictures
import cv2
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

# where do we store the images localy
IMAGES_DIR = "/home/pi/dev/scp/images/"
# width = 4056
# height = 3040
width = 3264
height = 2448
file_name=""
now = datetime.now()
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

# get configuration data from yaml file
def get_settings():

    # get G-Drive folder ID
    file = open(r'configuration.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    folder_id=conf_dic["folder_id"]
    logging.info("G-Drive folder ID:%s",folder_id)
    get_logic_sates_file(folder_id)
    # get system state data
    get_system_states()
    get_state_over_time()
    
# get file name by date
def get_file_name ():
    global file_name
    file_name =  now.strftime("%y-%m-%d__%H_%M")

# add timesamp to image (frame)
def put_date_time(file_name,image):
    display_time = now.ctime()
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (730,350)
    fontScale              = 5
    fontColor              = (0,0,0)
    lineType               = 5

    cv2.putText(image,display_time,
        bottomLeftCornerOfText,
        font,
        fontScale,
        fontColor,
        lineType)
    cv2.imwrite(file_name, image)


def get_logic_sates_file(folder_id):
    file_id = ""
    gauth = GoogleAuth()      
    # gauth.CommandLineAuth() # need this only one time per user, after that credentials are stored in credentials.json     
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
    for f in file_list:
        print('title: %s, id: %s' % (f['title'], f['id']))
        title = f['title']
        if title == "01 Commands":
            folder_id = f['id']
            file_list2 = drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
            for i in file_list2:
                print('title: %s, id: %s' % (i['title'], i['id']))
                title = i['title']
                if title == "logic_states.yaml":
                    file_id = i['id']
    if file_id == "":
        logging.error("unable to find logic_states.yaml on G-Drive")
    else:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile('logic_states.yaml') 

# upload image file into G-Drive
def upload_drive(folder_id,file_name,title_name):
    gauth = GoogleAuth()      
    # gauth.CommandLineAuth() # need this only one time per user, after that credentials are stored in credentials.json     
    drive = GoogleDrive(gauth)
    d_fileParams={}
    d_folderID={}
    d_folderID ["id"]=folder_id
    d_fileParams["parents"] = [d_folderID]
    d_fileParams["title"]= title_name
    gfile = drive.CreateFile(d_fileParams)
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(file_name)
    gfile.Upload() # Upload the file.
    logging.info("uploaded %s to drive",file_name)

# take a single picture from camera
def take_pic(cam_index, flip, focus, iso, exposure):
    
    global file_name 
    logging.info("taking picture from cam:%d focus:%d iso:%d exposure:%d",cam_index, focus, iso, exposure)
    
    new_file_name=file_name+"_c"+str(cam_index)+ ".txt" 
    saved_file_name = IMAGES_DIR + new_file_name
    f = open(saved_file_name, "a")
    f.close()
    upload_drive(folder_id, saved_file_name,new_file_name)
    
    # we have an issue with the cameras...so return
    return
    
    # select the camera
    camera = cv2.VideoCapture(cam_index)
    # set camera properties
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # wait 5 sec for the cam to focus
    time.sleep(5)
    # take pic
    return_value, image = camera.read()
    if flip:
        image = cv2.flip(image,-1)
    new_file_name=file_name+"_c"+str(cam_index)+ ".jpg"
    saved_file_name = IMAGES_DIR + new_file_name
    cv2.imwrite(saved_file_name,image)
    put_date_time(saved_file_name,image)
    upload_drive(folder_id, saved_file_name,new_file_name)
    camera.release()

def main():
    setup_logging()
    logging.info('*** Start ***')
    # get_file_name()
    # get_settings()
    camera = CameraHandler('A')
    camera.take_pic(20,"_122")
    # camera.take_pic(1000,"_")
    # camera.change_active_camera('C')
    # camera.take_pic(20,"_")
    # camera.take_pic(1000,"_")
    
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

    # logging.error("hello")
    # print("hello")
