from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import sys

import logging


RAW_IMAGES_FOLDER = "03 Raw Images"
COMMANDS_FOLDER = "01 Commands"
RAW_TELEMETRY_FOLDER = "02 Raw Telemetry"
FOLDER_ID="1TeYo5TB0DSDe4QAPa_7Wjta79ZxSd4pQ"

class GDriveHandler:

    main_folder_id = ""
    raw_images_folder_id = ""
    drive = None 

    # main_folder_id - the google drive folder ID. it should include "01 Commands" folder and the file logic_states.yaml in it 
    def __init__(self,main_folder_id):
        gauth = GoogleAuth(http_timeout=60)      
        gauth.CommandLineAuth() # need this only one time per user, after that credentials are stored in credentials.json     
        self.drive = GoogleDrive(gauth)
        self.main_folder_id = main_folder_id
        self.get_raw_images_folder_id()

    # create a new folder in G-Drive
    # title - The name of the folder
    # folder_id - The G-Drive parent folder id
    # return - True if sucess otherwise False
    def create_folder(self,title,folder_id):
        try: 
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth() 
            drive = GoogleDrive(gauth)

            file_metadata = {
            'title': title,
            'parents':  [{'id': folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = drive.CreateFile(file_metadata)
            folder.Upload()
            return True
        except:
            logging.error("Failed to create folder")
            return False

    def create_experiment_struct(self,experiment_name):
        try:
            if self.create_folder(experiment_name,FOLDER_ID):
             self.create_folder(COMMANDS_FOLDER,self.get_folder_id(experiment_name,FOLDER_ID))
             self.upload_file("configuration.yaml","configuration.yaml",self.get_folder_id(COMMANDS_FOLDER,self.get_folder_id(experiment_name,FOLDER_ID)))
             self.upload_file("logic_states.yaml","logic_states.yaml",self.get_folder_id(COMMANDS_FOLDER,self.get_folder_id(experiment_name,FOLDER_ID)))
             self.create_folder(RAW_TELEMETRY_FOLDER,self.get_folder_id(experiment_name,FOLDER_ID))
             self.create_folder(RAW_IMAGES_FOLDER,self.get_folder_id(experiment_name,FOLDER_ID))
             return True
        except:
            logging.error("Failed to create experiment struct")
            return False

    
    # upload file into G-Drive
    def upload_file(self,file_name,title_name,folder_id):
        logging.info("About to upload file:%s title:%s",file_name,title_name)
        try:
            d_fileParams={}
            d_folderID={}
            d_folderID ["id"]=folder_id
            d_fileParams["parents"] = [d_folderID]
            d_fileParams["title"]= title_name
            gfile = self.drive.CreateFile(d_fileParams)
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(file_name)
            gfile.Upload() # Upload the file.
            logging.info("uploaded %s to drive",file_name)
        except:
            logging.error("timeout while uploading file to G Drive")
    
    # upload image file into G-Drive
    def upload_image(self,file_name,title_name):
        self.upload_file(file_name,title_name,self.raw_images_folder_id)
    

    def get_folder_id(self,folder_name,parents_folder_id):
        file_id = ""
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %parents_folder_id}).GetList()
        for f in file_list:
            logging.debug('title: %s, id: %s' % (f['title'], f['id']))
            title = f['title']
            if title == folder_name:
                return f['id']

    # get the raw images folder if from G-Drive
    def get_raw_images_folder_id(self):
        id = self.get_folder_id(RAW_IMAGES_FOLDER,self.main_folder_id)
        if id == "":
            logging.error("unable to find Raw Images folder on G-Drive")
        else:
            self.raw_images_folder_id = id
            logging.info("Raw images folder id:%s",self.raw_images_folder_id)

    # get the logic_states.yaml file for G-Drive
    def get_logic_sates_file(self):
        logging.info("Getting logic_states.yaml from G-Drive...")
        folder_id = self.main_folder_id
        file_id = ""
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
        for f in file_list:
            logging.debug('title: %s, id: %s' % (f['title'], f['id']))
            title = f['title']
            if title == COMMANDS_FOLDER:
                folder_id = f['id']
                file_list2 = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
                for i in file_list2:
                    logging.debug('title: %s, id: %s' % (i['title'], i['id']))
                    title = i['title']
                    if title == "logic_states.yaml":
                        file_id = i['id']
        if file_id == "":
            logging.error("unable to find logic_states.yaml on G-Drive")
        else:
            file = self.drive.CreateFile({'id': file_id})
            file.GetContentFile('logic_states.yaml') 

    # get the configuration.yaml file for G-Drive
    def get_configuration_file(self):
        logging.info("Getting configuration.yaml from G-Drive...")
        folder_id = self.main_folder_id
        file_id = ""
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
        for f in file_list:
            logging.debug('title: %s, id: %s' % (f['title'], f['id']))
            title = f['title']
            if title == COMMANDS_FOLDER:
                folder_id = f['id']
                file_list2 = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
                for i in file_list2:
                    logging.debug('title: %s, id: %s' % (i['title'], i['id']))
                    title = i['title']
                    if title == "configuration.yaml":
                        file_id = i['id']
        if file_id == "":
            logging.error("unable to find configuration.yaml on G-Drive")
        else:
            file = self.drive.CreateFile({'id': file_id})
            file.GetContentFile('configuration.yaml') 

    # download images by start date, end date, list cameras, list focuses, path
    def download_images (self,start_date, end_date, list_camera, list_focus,my_path):
        self.get_raw_images_folder_id()
        folder_id = self.raw_images_folder_id
        logging.info('folder_id: %s' ,folder_id )

        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
        for f in file_list:
            #logging.debug('title: %s, id: %s' % (f['title'], f['id']))
            title = f['title']
            info_image=title.split("_C")
            #logging.info('info_image: %s' ,info_image)
            date_image=info_image[0]
            date_image_new= datetime.strptime(date_image,"%y-%m-%d__%H_%M")
            #logging.info('date_image_new %s' ,date_image_new)
            camera_image=info_image[1][0]
            #logging.info('camera_image: %s' ,camera_image)
            focus_image=int(info_image[1][3:7])
            #logging.info('focus_image: %s' ,focus_image)
            if date_image_new>=start_date and date_image_new<=end_date:
                if camera_image in list_camera:
                    if focus_image in list_focus:
                        logging.debug('about to download title: %s, id: %s' % (f['title'], f['id']))
                        file = self.drive.CreateFile({'id': f['id']})
                        file.GetContentFile(my_path+'/'+f['title'])

    def testDownloadFIle(self):
        file1 = self.drive.CreateFile({'id': '1zUKIfcAP3jIFr6w-sZHwzWyAwd74OwVo'}) #1ICaPnA5Yw5V5IpQb4r_vCq-Pgl6vjk2W

        # Fetches all basic metadata fields, including file size, last modified etc.
        # file1.FetchMetadata()

        # # Fetches all metadata available.
        # file1.FetchMetadata(fetch_all=True)

        # Fetches the 'permissions' metadata field.
        # file1.FetchMetadata(fields='permissions')
        # # You can update a list of specific fields like this:
        # file1.FetchMetadata(fields='permissions,labels,mimeType')
        print(file1['mimeType'])
        file1.GetContentFile('down_images/test12.jpg')

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("gdrive.log"),
            logging.StreamHandler()
        ]
    )   


if __name__ == "__main__":
    

    #quit()
    setup_logging()
    # logging.info("start g-drive testing")
    g_drive_handler = GDriveHandler("1usWtERCev43R107ccgdIZG83ORlwGnyB")
    g_drive_handler.create_experiment_struct("hadas10")
    #print(g_drive_handler.get_raw_images_folder_id())
    # # usage example: python3 gdrive_handler.py 21-09-10__13_56 21-09-10__13_58 A,B 260 images
    # if len(sys.argv)==6:
    #     start_date = sys.argv[1]
    #     start_date_new = datetime.strptime(start_date,"%y-%m-%d__%H_%M")
    #     end_date = sys.argv[2]
    #     end_date_new = datetime.strptime(end_date,"%y-%m-%d__%H_%M")
    #     list_camera = sys.argv[3]
    #     list_camera_new=list_camera.split(",")
    #     list_focus = sys.argv[4]
    #     list_focus_split = list_focus.split(",")
    #     list_focus_new = [int(i) for i in list_focus_split]
    #     my_path = sys.argv[5]
    #     print(start_date_new,end_date_new,list_camera_new,list_focus_new)
    #     g_drive_handler.download_images(start_date_new,end_date_new,list_camera_new,list_focus_new,my_path)
    # else:
    #     print("please enter 6 parameters:file name, start date, end date, list cameras, list focuses, path")
    #     print("for example: python3 gdrive_handler.py 21-09-14__06_20 21-09-14__06_22 A 160 /home/pi/dev/flight-software/down_images")
    #     quit()