import logging
import camera_handler
import RPi.GPIO as gp
import os
import time
from datetime import datetime
import threading
import yaml
from camera_handler import CameraHandler

import sys
sys.path.insert(1, '../common')
from focus_setting import FocusSetting


# This module builds on camrea_handler.py to implement higher level functionality such as distance to focus value
class CameraHandlerHighLevel:

    # Camera ids
    # By default, no camera is connected. Set their ids to be empty
    camera_A_id = ''
    camera_B_id = ''
    camera_C_id = ''
    camera_D_id = ''
    
    camera_A_focus_setting = []
    camera_B_focus_setting = []
    camera_C_focus_setting = []
    camera_D_focus_setting = []
    
    camera_handler = None

    # Constructor
    def __init__(self):
    
        # Read configuration file to understand what cameras are installed
        file = open(r'configuration.yaml')
        conf_dic = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        self.camera_A_id = conf_dic["camera_A_id"]
        self.camera_B_id = conf_dic["camera_B_id"]
        self.camera_C_id = conf_dic["camera_C_id"]
        self.camera_D_id = conf_dic["camera_D_id"]
        
        # Load focus settings for each installed camera
        if self.camera_A_id:
            self.camera_A_focus_setting = FocusSetting(self.camera_A_id)
        if self.camera_B_id:
            self.camera_B_focus_setting = FocusSetting(self.camera_B_id)
        if self.camera_C_id:
            self.camera_C_focus_setting = FocusSetting(self.camera_C_id)
        if self.camera_D_id:
            self.camera_D_focus_setting = FocusSetting(self.camera_D_id)
    
    def init_camera_handler(self):
        self.camera_handler = CameraHandler()
    
    # Get a list of connected cameras
    def get_enabled_cameras(self):
        enabled_cameras = []
        
        if self.camera_A_id:
            enabled_cameras.append('A')
        if self.camera_B_id:
            enabled_cameras.append('B')
        if self.camera_C_id:
            enabled_cameras.append('C')
        if self.camera_D_id:
            enabled_cameras.append('D')
        
        return enabled_cameras
        
    # Get camera id by connected position ('A','B','C','D')
    def get_camera_id_by_position(self,pos):
        if pos == 'A':
            return self.camera_A_id
        if pos == 'B':
            return self.camera_B_id
        if pos == 'C':
            return self.camera_C_id
        if pos == 'D':
            return self.camera_D_id
            
    # Returns the focus setting that is needed for a specific camera given the imaging distance
    # Inputs are:
    #   camera position 'A','B','C' or 'D'
    #   distance to convert to focus setting
    def get_camera_focus_setting(self,pos,distance_mm):
        if pos == 'A':
            return self.camera_A_focus_setting.focus_distance_to_setting(distance_mm)
        if pos == 'B':
            return self.camera_B_focus_setting.focus_distance_to_setting(distance_mm)
        if pos == 'C':
            return self.camera_C_focus_setting.focus_distance_to_setting(distance_mm)
        if pos == 'D':
            return self.camera_D_focus_setting.focus_distance_to_setting(distance_mm)
        
    # Take picture using cameras of some focus distance
    # Inputs are:
    #   camera position 'A','B','C' or 'D'
    #   the list of distances to take images at in mm. e.g: [50, 100]  
    #   file_name_prefix is usually the date
    def take_pic_all_distances (self, camera_pos, distance_list_mm, file_name_prefix = "test"):
        # Init
        files_list=[]

        # Set active camera 
        self.camera_handler.change_active_camera(camera_pos)
        
        # Loop over all distances
        for d in distance_list_mm:
            f = self.get_camera_focus_setting(camera_pos, d)
            self.camera_handler.change_focus(f)
            full_path_file_name,title_name = self.camera_handler.take_pic(file_name_prefix,True)
            files_list.append((full_path_file_name,title_name))
            
        # Return the files we generated
        return files_list
  

# Auxilery function for testing
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("scp_main.log"),
            logging.StreamHandler()
        ]
    )  
    
if __name__ == "__main__":
    setup_logging()
    camera_handler_high_level = CameraHandlerHighLevel()

    list_of_enabled_cameras = camera_handler_high_level.get_enabled_cameras()
    print(list_of_enabled_cameras[0])
    
    distance_mm = 100
    print('Camera A')
    camera_handler_high_level.take_pic_all_distances('A',[distance_mm])
    print('Camera B')
    camera_handler_high_level.take_pic_all_distances('B',[distance_mm])
    print('Camera C')
    camera_handler_high_level.take_pic_all_distances('C',[distance_mm])
    print('Camera D')
    camera_handler_high_level.take_pic_all_distances('D',[distance_mm])
    