import yaml
import os
from gdrive_handler import GDriveHandler
import logging
import shutil
import glob
import os
import time

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


def delete_old_files():
  #  dir_name = '/home/pi/dev/flight-software'
    # Get list of all files only in the given directory
  #  list_of_files = filter( os.path.isfile,
     #                       glob.glob(dir_name + '*') )
    # Sort list of files based on last modification time in ascending order
 #   list_of_files = sorted( list_of_files,
   #                        key = os.path.getmtime)
    # Iterate over sorted list of files and print file path 
    # along with last modification time of file 
  #  for file_path in list_of_files:
  #      timestamp_str = time.strftime(  '%m/%d/%Y :: %H:%M:%S',
 #                                   time.gmtime(os.path.getmtime(file_path))) 
   #     print(timestamp_str, ' -->', file_path) 

    file_list = os.listdir('/home/pi/dev/flight-software')
    print (file_list)

    #grab last 4 characters of the file name:
    def last_4chars(x):
        return(x[-4:])

    file_list_sort = sorted(file_list, key = last_4chars)
    print (file_list_sort)

def check_free_space():  
    # Path
    path = "/home"
    
    # Get the disk usage statistics
    # about the given path
    stat = shutil.disk_usage(path)
    
    # Print disk usage statistics
    print("Disk usage in %:")
    print(stat.used/stat.total*100)


if __name__ == "__main__":

    check_free_space()
    delete_old_files()


    # setup_logging()
    # uploaded_files = read_uploaded_files()
    # files = get_file_name("images")
    # g_drive_handler = GDriveHandler(getGDrive_folder_id())
    # f = open("uploaded_files.log", "a")    

    # for f_name in files:
    #     if uploaded_files.get(f_name+'\n') == None:
    #         g_drive_handler.upload_file("images/"+f_name,f_name)
    #         f.write(f_name+'\n')
    #         f.flush()
    #     else:
    #         print("allready uploaded file:",f_name)

    # f.close()  