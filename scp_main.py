# Read yaml configurtation files, based on the schedule, setup lesds, take pictures


import cv2
import time
from datetime import datetime
import board
import neopixel
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import yaml
from system_state import SystemState 
from system_state import CameraConfiguration
from system_state import FocusPosition

# width = 4056
# height = 3040
width = 3264
height = 2448
file_name=""
pixels = neopixel.NeoPixel(board.D18, 12,brightness=2)
now = datetime.now()
# g-drive folder ID
folder_id = ""
# holds system states configurations
system_states={}

# read all system states from yaml file and load into memory
def getSystemStates():
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
         


# get configuration data from yaml file
def get_settings():

    # get G-Drive folder ID
    global folder_id
    file = open(r'configuration.yaml')
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    folder_id=conf_dic["folder_id"]
    print(folder_id)

    # get system state data
    getSystemStates()

# get file name by date
def get_file_name ():
    global file_name
    file_name =  now.strftime("%y_%m_%d__%H_%M_%S")

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

# take a single picture from camera
def take_pic(cam_index, flip, focus, iso, exposure):
    
    global file_name 
    print("taking picture from cam",cam_index, focus, iso, exposure)
    path = "/home/pi/dev/scp/images/"
    new_file_name=file_name+"_c"+str(cam_index)+ ".txt" 
    saved_file_name = path + new_file_name
    f = open(saved_file_name, "a")
    upload_drive(folder_id, saved_file_name,new_file_name)
    print("upload to drive")

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
    path = "/home/pi/dev/scp/images/" 
    new_file_name=file_name+"_c"+str(cam_index)+ ".jpg"
    saved_file_name = path + new_file_name
    print("saving to:",saved_file_name)
    cv2.imwrite(saved_file_name,image)
    put_date_time(saved_file_name,image)
    upload_drive(folder_id, saved_file_name,new_file_name)
    print("upload to drive")
    camera.release()

    print("end taking picture, file saved:",saved_file_name)

def start_LED ():
    pixels.fill((255, 255, 255))

def stop_LED():
    pixels.fill((0, 0, 0))


def main():
    get_file_name()
    get_settings()
    start_LED ()
    for f in range(100,101,1):
        take_pic(0,False,f,5,5)
        take_pic (1,True,f,10,10)
    stop_LED()


if __name__ == "__main__":
    main()
