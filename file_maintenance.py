import yaml
import os
from gdrive_handler import GDriveHandler
import logging
import shutil
import glob
import os
import time

CONF_FILE_NAME = "scp_conf.yaml"
IMAGES_PATH = '/home/pi/dev/flight-software/images'
MAX_USED_SPACE_ALLOWED = 80 # in percent

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


def delete_old_files(path):

    def last_created(x):
        return(x[1])
 
    def file_info():
        file_list = []
        for i in os.listdir(path):
            a = os.stat(os.path.join(path,i))
            file_list.append([i,a.st_ctime]) #[file,most_recent_access,created]
        return file_list

    file_list = file_info()
  
    file_list_sort = sorted(file_list, key = last_created)

    # for item in file_list_sort:
    #     line = "Name: {:<20} | Date Created: {:>20}".format(item[0],time.ctime(item[1]))
    #     print(line)

    if len(file_list_sort) > 0 :
      file_to_del=path+'/'+file_list_sort[0][0]
      logging.debug("about to delete file:%s",file_to_del)
      os.remove(file_to_del)


def check_used_space(path):  
    # Get the disk usage statistics
    # about the given path
    stat = shutil.disk_usage(path)
    
    # Print disk usage statistics
    used_space = int(stat.used/stat.total*100)
    logging.debug("used disk space:%d%%",used_space) 
    return used_space


if __name__ == "__main__":
    setup_logging()
    used_space = check_used_space(IMAGES_PATH)
    while used_space > MAX_USED_SPACE_ALLOWED:  
        delete_old_files(IMAGES_PATH)
        used_space = check_used_space(IMAGES_PATH)
        time.sleep(1)


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