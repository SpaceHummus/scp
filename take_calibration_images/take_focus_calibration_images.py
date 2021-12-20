
# Add paths to flight software and common, we need these modules later on
import sys
sys.path.insert(1, '../common')
sys.path.insert(1, '../flight_software')

# Main imports of this code
import camera_handler
import time
import string
import numpy as np
import os
import logging
import shutil

# General configuration of this script, these numbers should match .gcode
#########################################################################

# Height above pattern for each image set
camera_heights_mm = [40, 50, 60, 70, 80, 90, 100, 110 , 120] 

# What camera focus positions should we try?
camera_focus_settings = range(0,401,20)

# Time it takes to complete image aquisition
time_per_image_set_sec = 300


def create_image_folder_if_not_exist(path):
    is_exist = os.path.exists(path)
    
    if  is_exist:
        shutil.rmtree(path)
    
    os.makedirs(path)   
        
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("calibration_images.log"),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    camera = camera_handler.CameraHandler()
    camera.change_active_camera('A')

    # Get input from user about the camera we will use today
    print("What is the camera serial number we will calibrate today (Example: C01)?")
    camera_sn = input("")
    camera_sn = camera_sn.upper()
    print("Selected '{0}'".format(camera_sn))
    time.sleep(1)
    
    # Create output folder
    output_folder_path = "{0}_focus_calibration_images_{1}/".format(camera_sn,time.strftime("%Y-%m-%d"))
    create_image_folder_if_not_exist(output_folder_path)
    
    # Ask user to start robot
    print("Place Rotric's arm against the ipad presenting focus strips")
    print("On Rotric's consule run take_focus_calibration_images.gcode")
    val = input("Press Enter when robot is lifted to it's first position ({0} mm)".format(camera_heights_mm[0]) )
    
    # Loop over all heights
    for camera_height_mm in camera_heights_mm:
        aquisition_start_time = time.time()
        print("Taking images for height of {0} mm".format(camera_height_mm))
        
        # Loop over focus positions
        for camera_focus_setting in camera_focus_settings:
            # Change focus
            camera.change_focus(camera_focus_setting)
            
            # Take a picture
            image_file_name_prefix = "h{0:03d}mm".format(camera_height_mm)
            camera.take_pic(image_file_name_prefix,file_directory=output_folder_path)
            
            t=time.time()
            print(t-aquisition_start_time)
        
        # Notify user 
        print("  Aquisition done, move to next height")
        
        # Before moving to the next height, check how much time is left in order to synch with the robot
        aquisition_end_time = time.time()
        time_left = time_per_image_set_sec - (aquisition_end_time - aquisition_start_time)
        if time_left < 2:
            print("ERROR - ran out of time, please increase time_per_image_set_sec")
            return
        time.sleep(time_left)
        
    print("All Done")
    
if __name__ == "__main__":
    main()