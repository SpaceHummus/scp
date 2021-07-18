import os
import time
import sys
import threading
from ctypes import *
arducam_vcm =CDLL('./lib/libarducam_vcm.so')

def run_camera(name):
    os.system("raspistill -t 4000")

if __name__ == "__main__":
    focus_val = 260
    arducam_vcm.vcm_init()
    # thread.start_new_thread(run_camera, ("run_camera",))
    x = threading.Thread(target=run_camera, args=(1,))
    x.start()
    time.sleep(2)
    arducam_vcm.vcm_write(focus_val)
    time.sleep(3)
    os.system("raspistill -o %d.jpg"%focus_val)
    
    
    
    
    
    # thread.start_new_thread(run_camera, ("run_camera",))
    # focus_val = 260
    # time.sleep(1)
    # arducam_vcm.vcm_write(focus_val)
    # time.sleep(3)
    # os.system("raspistill -o %d.jpg"%focus_val)

