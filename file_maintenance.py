import yaml
import os
from gdrive_handler import GDriveHandler
import logging
import shutil
import glob
import os
import time
import pidfile

CONF_FILE_NAME = "scp_conf.yaml"
IMAGES_PATH = '/home/pi/dev/flight-software/images'
MAX_USED_SPACE_ALLOWED = 85 # in percent

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

def get_files_name(dir_path):
    arr = os.listdir(dir_path)
    return arr



def read_uploaded_files():
    uploaded_files={}
    f = open("uploaded_files.log", "r")
    for x in f:
        uploaded_files[x] = 1
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

def main():
    # upload files that we didn't upload yet... 
    f = open("uploaded_files.log", "a")    
    try:
        uploaded_files = read_uploaded_files()
        files = get_files_name(IMAGES_PATH)
        
        g_drive_handler = GDriveHandler(getGDrive_folder_id())

        c = 0
        for f_name in files:
            if uploaded_files.get(f_name+'\n') == None: # meaning we have a file that we didn't upload yet
                if g_drive_handler.upload_image(IMAGES_PATH+"/"+f_name,f_name):
                    f.write(f_name+'\n')
                    f.flush()
                    c+=1
        logging.info("Uploaded %d files to g-drive",c)
    except Exception as e: 
        logging.error('unable to upload file to g-drive: '+ str(e))
    f.close()  

    # check and clear space on the SD card if needed
    used_space = check_used_space(IMAGES_PATH)
    while used_space > MAX_USED_SPACE_ALLOWED:  
        delete_old_files(IMAGES_PATH)
        used_space = check_used_space(IMAGES_PATH)
        time.sleep(1)


if __name__ == "__main__":
    setup_logging()
    try:
        with pidfile.PIDFile():
            main()
    except pidfile.AlreadyRunningError:
        logging.error('Process already running.')







