from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging

RAW_IMAGES_FOLDER = "03 Raw Images"
COMMANDS_FOLDER = "01 Commands"

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
        self.get_logic_sates_file()
        self.get_configuration_file()
        self.get_raw_images_folder_id()


    # upload image file into G-Drive
    def upload_file(self,file_name,title_name):
        logging.info("About to upload file:%s title:%s",file_name,title_name)
        try:
            d_fileParams={}
            d_folderID={}
            d_folderID ["id"]=self.raw_images_folder_id
            d_fileParams["parents"] = [d_folderID]
            d_fileParams["title"]= title_name
            gfile = self.drive.CreateFile(d_fileParams)
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(file_name)
            gfile.Upload() # Upload the file.
            logging.info("uploaded %s to drive",file_name)
        except:
            logging.error("timeout while uploading file to G Drive")

    # get the raw images folder if from G-Drive
    def get_raw_images_folder_id(self):
        folder_id = self.main_folder_id
        file_id = ""
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" %folder_id}).GetList()
        for f in file_list:
            logging.debug('title: %s, id: %s' % (f['title'], f['id']))
            title = f['title']
            if title == RAW_IMAGES_FOLDER:
                self.raw_images_folder_id = f['id']
        if self.raw_images_folder_id == "":
            logging.error("unable to find Raw Images folder on G-Drive")
        else:
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
