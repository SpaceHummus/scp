import logging
import camera_handler
import RPi.GPIO as gp
import os
import time
from datetime import datetime
import threading
import yaml
import focus_setting

# This module builds on camrea_handler.py to implement higher level functionality such as distance to focus value


class CameraHandlerHighLevel:

    # Camera ids
    # By default, no camera is connected. Set their ids to be empty
    camera_A_id = ''
    camera_B_id = ''
    camera_C_id = ''
    camera_D_id = ''

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
        

if __name__ == "__main__":
    camera = CameraHandlerHighLevel()

    list_of_enabled_cameras = camera.get_enabled_cameras()
    print(list_of_enabled_cameras[0])
    