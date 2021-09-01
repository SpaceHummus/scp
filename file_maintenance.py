import yaml
import os
from gdrive_handler import GDriveHandler
import logging

CONF_FILE_NAME = "scp_conf.yaml"


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("file_maintenance.log"),
            logging.StreamHandler()
        ]
    )    

def getGDrive_folder_id():
    # get G-Drive folder ID
    file = open(CONF_FILE_NAME,"r")
    conf_dic = yaml.load(file, Loader=yaml.FullLoader)
    folder_id=conf_dic["folder_id"]
    file.close()
    return folder_id

def get_file_name(dir_path):
    arr = os.listdir(dir_path)
    return arr



def read_uploaded_files():
    uploaded_files={}
    f = open("uploaded_files.log", "r")
    for x in f:
        print(x)
        uploaded_files[x] = 1
    print (uploaded_files)
    return uploaded_files




setup_logging()
uploaded_files = read_uploaded_files()
files = get_file_name("images")
g_drive_handler = GDriveHandler(getGDrive_folder_id())
f = open("uploaded_files.log", "a")

 

for f_name in files:
    if uploaded_files.get(f_name+'\n') == None:
        g_drive_handler.upload_file("images/"+f_name,f_name)
        f.write(f_name+'\n')
        f.flush()
    else:
        print("allready uploaded file:",f_name)

f.close()  