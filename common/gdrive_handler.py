import sys
# sys.path.append("E:/dev/credentials")
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.file import Storage
from datetime import datetime
import logging
import yaml


RAW_IMAGES_FOLDER = "03 Raw Images"
COMMANDS_FOLDER = "01 Commands"
RAW_TELEMETRY_FOLDER = "02 Raw Telemetry"

class GDriveHandler:

    main_folder_id = ""
    raw_images_folder_id = ""
    drive = None 

    # main_folder_id - the google drive folder ID. it should include "01 Commands" folder and the file logic_states.yaml in it 
    def __init__(self,main_folder_id):
        gauth = GoogleAuth(settings_file="../../credentials/settings.yaml",http_timeout=60)      
        gauth.credentials = Storage(f"../../credentials/credentials.json").get()
        gauth.CommandLineAuth() # need this only one time per user, after that credentials are stored in credentials.json     
        self.drive = GoogleDrive(gauth)
        self.main_folder_id = main_folder_id

    # create a new folder in G-Drive
    # title - The name of the folder
    # folder_id - The G-Drive parent folder id
    # return - True if sucess otherwise False
    def create_folder(self,title,folder_id):
        try: 

            file_metadata = {
            'title': title,
            'parents':  [{'id': folder_id}],
            'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive.CreateFile(file_metadata)
            folder.Upload()
            return True
        except Exception as e:
            logging.error("Failed to create folder. Error msg:%s",str(e))
            return False

    def create_experiment_struct(self,experiment_name,experiment_date):
        try:
            if self.create_folder(experiment_name,self.main_folder_id):
                experiment_folder_id = self.get_folder_id(experiment_name,self.main_folder_id)
                self.create_folder(COMMANDS_FOLDER,experiment_folder_id)
                cmd_folder_id = self.get_folder_id(COMMANDS_FOLDER,experiment_folder_id)
                self.upload_file("../interfaces/configuration.yaml","configuration.yaml",cmd_folder_id)
                self.update_logic_state_file(datetime.strptime(experiment_date,"%Y/%m/%d %H:%M:%S"))
                self.upload_file("logic_states_new_exp.yaml","logic_states.yaml",cmd_folder_id)
                self.create_folder(RAW_TELEMETRY_FOLDER,experiment_folder_id)
                self.create_folder(RAW_IMAGES_FOLDER,experiment_folder_id)
                return experiment_folder_id
        except Exception as e:
            logging.error("Failed to create experiment struct. Error msg:%s",str(e))
            return None

    def update_logic_state_file(self,start_date):
        states_over_time_new = []
        file = open(r'../interfaces/logic_states.yaml')
        conf_dic = yaml.load(file, Loader=yaml.FullLoader)
        states_over_time_orig = conf_dic["states_over_time"] 
        file.close()

        date_time_0 = datetime.strptime(states_over_time_orig[0][0],"%Y/%m/%d %H:%M:%S")
        for i in range(len(states_over_time_orig)):
            date_time_str = states_over_time_orig[i][0]
            date_time_obj = datetime.strptime(date_time_str,"%Y/%m/%d %H:%M:%S")
            updated_date = start_date + (date_time_obj-date_time_0)
            updated_date = updated_date.strftime('%Y/%m/%d %H:%M:%S')
            states_over_time_new.append([updated_date,states_over_time_orig[i][1]])

        conf_dic["states_over_time"] = states_over_time_new
        with open('logic_states_new_exp.yaml','w') as f:
            yaml.dump(conf_dic, f)

    # upload file into G-Drive
    def upload_file(self,file_name,title_name,folder_id):
        logging.info("About to upload file:%s title:%s folder_id:%s",file_name,title_name,folder_id)
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
            return True
        except Exception as e:
            logging.error("error uploading file to G Drive. Error msg:%s",str(e))
            return False
    
    # upload image file into G-Drive
    def upload_image(self,file_name,title_name):
        return self.upload_file(file_name,title_name,self.get_raw_images_folder_id())
    

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
        if self.raw_images_folder_id == "": # first time we ask for images folder ID
            id = self.get_folder_id(RAW_IMAGES_FOLDER,self.main_folder_id)
            if id == "":
                logging.error("unable to find Raw Images folder on G-Drive")
            else:
                self.raw_images_folder_id = id
                logging.info("Raw images folder id:%s",self.raw_images_folder_id)
                return self.raw_images_folder_id
        else:
            return self.raw_images_folder_id

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
        folder_id = self.get_raw_images_folder_id()
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
    setup_logging()
    logging.info("start g-drive")
    # usage example: python3 gdrive_handler.py new_exp [EXP_NAME] 
    if len(sys.argv)<=1:
        print("Please enter parameters:command [PARAM_1...PARAM_N]\n")
        print("supported commands: new_exp - create a new experiment with new folder structures. parametrs: <experiment name> <experiment date in YYYY/M/D hh:mm:ss> . prints the new folder id of the experiment\n")
        print("for example: python3 gdrive_handler.py new_exp \"2021-07-08 B0.1 Yerucham Dev1\" \"2021/07/15 10:00:00\"")
        quit()
    else:
        cmd = sys.argv[1]
        if cmd == "new_exp":
            if len(sys.argv)<=3:
                print("missing parameter")
                quit()
            g_drive_handler = GDriveHandler(ROOT_FOLDER_ID)
            f_id = g_drive_handler.create_experiment_struct(sys.argv[2],sys.argv[3])
            logging.info("created new experiment. its folder id is:%s",f_id)
        else:
            print("invalid command")
            quit()
