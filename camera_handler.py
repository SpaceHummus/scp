import logging
import RPi.GPIO as gp
import os
# from picamera.array import PiRGBArray
# from picamera import PiCamera
from ctypes import *
arducam_vcm =CDLL('./lib/libarducam_vcm.so')
import time
from datetime import datetime
import cv2

# where do we store the images localy
IMAGES_DIR = "/home/pi/dev/scp/images/"

class CameraHandler:
    activeCamera=''
    # camera = PiCamera()


    # Constructor, index='A'/'B'/'C'/'D'
    def __init__(self,camera_index,width=4056,height=3040):
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

        self.change_active_camera(camera_index)
        arducam_vcm.vcm_init()

        # self.camera.resolution = (width, height)
        # self.camera.iso = 100
        # time.sleep(5)
        # self.camera.shutter_speed = camera.exposure_speed
        # self.camera.exposure_mode = 'off'
        # g = self.camera.awb_gains
        # self.camera.awb_mode = 'off'
        # self.camera.awb_gains = g
        # self.camera.brightness = 30
        # arducam_vcm.vcm_init()


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

    # add timesamp to image (frame)
    def put_date_time(self,file_name,image):
        now = datetime.now()
        display_time = now.ctime()
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (730,350)
        fontScale              = 5
        fontColor              = (0,0,0)
        lineType               = 5

        cv2.putText(image,display_time,
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)
        cv2.imwrite(file_name, image)

    # take picture , camera_index='A'/'B'/'C'/'D'
    def take_pic(self, focus,file_name):
        time.sleep(0.1)
        arducam_vcm.vcm_write(focus)
        # setup file name with camera index and focus
        new_file_name="{0}_C{1}_F{2:04d}.jpg".format(file_name,self.activeCamera,focus) 
        saved_file_name = IMAGES_DIR + new_file_name
        logging.info("taking picture, image name:%s",saved_file_name)
        cmd = "raspistill -o %s" %saved_file_name 
        os.system(cmd)
        logging.info("done taking picture")
        # image = self.put_date_time(image)

        # upload_drive(folder_id, saved_file_name,new_file_name)
