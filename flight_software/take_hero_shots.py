import logging
import camera_handler
import RPi.GPIO as gp
import os
import time
from datetime import datetime
import threading
import yaml
import root_image_handler
import camera_handler_high_level


import sys
sys.path.insert(1, '../common')
from focus_setting import FocusSetting

class HeroShots:
    camera_A_focus_setting = [310]
    camera_B_focus_setting = [245]
    camera_C_focus_setting = [220]
    camera_D_focus_setting = [270]
    cam = [] 
    
    def __init__(self):
        self.cam = camera_handler_high_level.CameraHandlerHighLevel()
        self.cam.init_camera_handler()

    def hero_shot_cameras_abcd(self, hero_name, date_name, r_g_b_fr_mw):
        logging.info("Take {0}".format(hero_name))
        file_name_prefix="{1}_HeroShot_{0}".format(hero_name,date_name)
        
        self.cam.take_pic_all_focus('A',self.camera_A_focus_setting,
            file_name_prefix=file_name_prefix,
            r_g_b_fr_mw = r_g_b_fr_mw)
        time.sleep(1)
        self.cam.take_pic_all_focus('B',self.camera_B_focus_setting,
            file_name_prefix=file_name_prefix,
            r_g_b_fr_mw = r_g_b_fr_mw)
        time.sleep(1)
        self.cam.take_pic_all_focus('C',self.camera_C_focus_setting,
            file_name_prefix=file_name_prefix,
            r_g_b_fr_mw = r_g_b_fr_mw)
        time.sleep(1)
        self.cam.take_pic_all_focus('D',self.camera_D_focus_setting,
            file_name_prefix=file_name_prefix,
            r_g_b_fr_mw = r_g_b_fr_mw)
        time.sleep(1)


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
    
def take_all_shots():
    setup_logging()
    hs = HeroShots()
  
    # Make sure every shot has the same name
    now = datetime.now()
    date_name = now.strftime("%y-%m-%d__%H_%M")

    # Kill main process
    logging.info("Killing SCP main")
    os.system('./stop_scp_main.sh')
    time.sleep(10) # Make sure it's dead
    
    hs.hero_shot_cameras_abcd('WhiteLight',date_name,[100, 100, 100, 0, 0])
    hs.hero_shot_cameras_abcd('HotRed1',date_name,[0, 0, 0, 10, 0])
    hs.hero_shot_cameras_abcd('Backlight1',date_name,[0, 0, 0, 0, 1])
    hs.hero_shot_cameras_abcd('Backlight2',date_name,[100, 100, 100, 0, 1])

    
if __name__ == "__main__":
     take_all_shots()
    