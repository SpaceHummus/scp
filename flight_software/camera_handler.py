from ast import Return
import logging
import RPi.GPIO as gp
import os
from ctypes import *
arducam_vcm =CDLL('./lib/libarducam_vcm.so')
import time
from datetime import datetime
import threading
from pathlib import Path


# where do we store the images localy
IMAGES_DIR = "images/"

def run_camera(name):
    os.system("raspistill -t 2000")


# check if the image file name already exists, if yes, generate a new one
def fix_file_path(file_path: str) -> str:
    file = Path(file_path)
    if not file.exists():
        return str(file)
    year = 10
    name = file.name[2:]
    while year<100: # up to year 99 (2099)
        new_path = file.parent / f"{year}{name}"
        if not new_path.exists():
            return str(new_path)
        year +=1
    return str(file.parent / f"{year}{name}")

# convert board pin numbering to bcm numbering
def board3bcm(pin):
    if pin==7:
        return 4
    elif pin == 11:
        return 17
    elif pin == 12:
        return 18
    elif pin == 15:
        return 22
    elif pin == 16:
        return 23
    elif pin == 21:
        return 9
    elif pin == 22:
        return 25


class CameraHandler:
    activeCamera='A'
    focus=512

    # Constructor, index='A'/'B'/'C'/'D'
    def __init__(self,width=4056,height=3040):
        gp.setwarnings(False)
        gp.setmode(gp.BCM)

        gp.setup(board3bcm(7), gp.OUT)
        gp.setup(board3bcm(11), gp.OUT)
        gp.setup(board3bcm(12), gp.OUT)

        gp.setup(board3bcm(15), gp.OUT)
        gp.setup(board3bcm(16), gp.OUT)
        gp.setup(board3bcm(21), gp.OUT)
        gp.setup(board3bcm(22), gp.OUT)

        gp.output(board3bcm(11), True)
        gp.output(board3bcm(12), True)
        gp.output(board3bcm(15), True)
        gp.output(board3bcm(16), True)
        gp.output(board3bcm(21), True)
        gp.output(board3bcm(22), True)

        arducam_vcm.vcm_init()

    # switch active cameras, index='A'/'B'/'C'/'D'
    def change_active_camera(self,camera_index):
        self.activeCamera = camera_index
        logging.info("changing active camera to:%s",camera_index)
        if camera_index=='A':
            i2c = "i2cset -y 1 0x70 0x00 0x04"
            os.system(i2c)
            gp.output(board3bcm(7), False)
            gp.output(board3bcm(11), False)
            gp.output(board3bcm(12), True)
        elif camera_index=='B':
            i2c = "i2cset -y 1 0x70 0x00 0x05"
            os.system(i2c)
            gp.output(board3bcm(7), True)
            gp.output(board3bcm(11), False)
            gp.output(board3bcm(12), True)
        elif camera_index=='C':
            i2c = "i2cset -y 1 0x70 0x00 0x06"
            os.system(i2c)
            gp.output(board3bcm(7), False)
            gp.output(board3bcm(11), True)
            gp.output(board3bcm(12), False)
        elif camera_index=='D':
            i2c = "i2cset -y 1 0x70 0x00 0x07"
            os.system(i2c)
            gp.output(board3bcm(7), True)
            gp.output(board3bcm(11), True)
            gp.output(board3bcm(12), False)
        else:
            logging.error("invalid camera index %s",camera_index)

    # Change camera focus - due to a bug in the HW, we need to open a thread that starts raspstill in the backbround inparallel, why??? who knows...
    def change_focus(self,focus):
        self.focus = focus
        logging.info("changing focus to:%d",focus)
        x = threading.Thread(target=run_camera, args=(1,))
        x.start()
        time.sleep(2)
        arducam_vcm.vcm_write(focus)
        time.sleep(3)

    # take picture , camera_index='A'/'B'/'C'/'D'
    # make sure you first call change_active_camera & change_focus
    # return full path saved file, file name
    def take_pic(self, file_name, flip_image=False, file_directory=IMAGES_DIR):
        # Generate file name and path string
        new_file_name="{0}_C{1}_F{2:04d}.jpg".format(file_name,self.activeCamera,self.focus)
        saved_file_name = fix_file_path(file_directory + new_file_name)

        # Aquire image
        logging.info("taking picture, image name:%s",saved_file_name)
        if flip_image:
            cmd = "raspistill -vf -hf -o %s" %saved_file_name
        else:
            cmd = "raspistill -o %s" %saved_file_name
        os.system(cmd)
        logging.info("done taking picture")

        return saved_file_name, new_file_name



if __name__ == "__main__":
    camera = CameraHandler()

    print("A")
    camera.change_active_camera('A')
    camera.change_focus(200)
    camera.take_pic("22-02-01__15_54")
    camera.change_focus(1000)
    camera.take_pic("22-02-01__15_54")
    quit()
    print("B")
    camera.change_active_camera('B')
    camera.change_focus(200)
    camera.take_pic("test_take_out_jumpers")
    camera.change_focus(1000)
    camera.take_pic("test_take_out_jumpers")

    print("C")
    camera.change_active_camera('C')
    camera.change_focus(200)
    camera.take_pic("test_take_out_jumpers")
    camera.change_focus(1000)
    camera.take_pic("test_take_out_jumpers")

    print("D")
    camera.change_active_camera('D')
    camera.change_focus(200)
    camera.take_pic("test_take_out_jumpers")
    camera.change_focus(1000)
    camera.take_pic("test_take_out_jumpers")
