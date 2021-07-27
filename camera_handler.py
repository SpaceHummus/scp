import logging
import RPi.GPIO as gp
import os
from ctypes import *
arducam_vcm =CDLL('./lib/libarducam_vcm.so')
import time
from datetime import datetime
import threading

# where do we store the images localy
IMAGES_DIR = "images/"

def run_camera(name):
    os.system("raspistill -t 2000")

class CameraHandler:
    activeCamera=''
    focus=512

    # Constructor, index='A'/'B'/'C'/'D'
    def __init__(self,camera_index,focus=512,width=4056,height=3040):
        gp.setwarnings(False)
        gp.setmode(gp.BOARD)

        gp.setup(7, gp.OUT)
        gp.setup(11, gp.OUT)
        gp.setup(12, gp.OUT)

        gp.setup(15, gp.OUT)
        gp.setup(16, gp.OUT)
        gp.setup(21, gp.OUT)
        gp.setup(22, gp.OUT)

        gp.output(11, True)
        gp.output(12, True)
        gp.output(15, True)
        gp.output(16, True)
        gp.output(21, True)
        gp.output(22, True)

        arducam_vcm.vcm_init()

        self.change_active_camera(camera_index)
        self.change_focus(focus)

    # switch active cameras, index='A'/'B'/'C'/'D'
    def change_active_camera(self,camera_index):
        self.activeCamera = camera_index
        logging.info("changing active camera to:%s",camera_index)
        if camera_index=='A':
            i2c = "i2cset -y 1 0x70 0x00 0x04"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, False)
            gp.output(12, True)
        elif camera_index=='B':
            i2c = "i2cset -y 1 0x70 0x00 0x05"
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, False)
            gp.output(12, True)
        elif camera_index=='C':
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(7, False)
            gp.output(11, True)
            gp.output(12, False)
        elif camera_index=='D':
            i2c = "i2cset -y 1 0x70 0x00 0x07"
            os.system(i2c)
            gp.output(7, True)
            gp.output(11, True)
            gp.output(12, False)
        else:
            logging.error("invalid camera index %s",camera_index)

    # change camera focus - due to a bug in the HW, we need to open a thread that starts raspstill in the backbround inparallel, why??? who knows...
    def change_focus(self,focus):
        self.focus = focus
        logging.info("changing focus to:%d",focus)        
        x = threading.Thread(target=run_camera, args=(1,))
        x.start()
        time.sleep(2)
        arducam_vcm.vcm_write(focus)
        time.sleep(3)

    # take picture , camera_index='A'/'B'/'C'/'D'
    # return full path saved file, file name
    def take_pic(self, file_name, flip_image=False):
        # setup file name with camera index and focus
        new_file_name="{0}_C{1}_F{2:04d}.jpg".format(file_name,self.activeCamera,self.focus) 
        saved_file_name = IMAGES_DIR + new_file_name
        logging.info("taking picture, image name:%s",saved_file_name)
        if flip_image:
            cmd = "raspistill -vf -hf -o %s" %saved_file_name
        else:
            cmd = "raspistill -o %s" %saved_file_name 
        os.system(cmd)
        logging.info("done taking picture")
        return saved_file_name, new_file_name
