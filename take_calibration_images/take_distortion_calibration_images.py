
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

# General configuration of this script, these numbers should match .gcode
#########################################################################

# Number of x-y robot positions
n_robot_positions = 49

# Z positions & camera focus positions (for each height one focus position)
camera_height_above_iPad_mm = [110,  80,  65,  58,  52]
camera_focus_settings =       [110, 150, 190, 210, 230]

# Time it takes to complete image aquisition for each x-y position
time_per_image_set_sec = 10

def create_image_folder_if_not_exist(path):
    is_exist = os.path.exists(path)
    
    if not is_exist:
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
    output_folder_path = "{0}_distortion_calibration_images_{1}/".format(camera_sn,time.strftime("%Y-%m-%d"))
    create_image_folder_if_not_exist(output_folder_path)
    
    # Ask user to start robot
    print("")
    print("Make shure the robot is centered at the pattern")
    print("On Rotric's consule run take_distortion_calibration_images.gcode")
    val = input("Press Enter when robot is finished moving to the center position")
    
    # Loop over all heights
    for i in range(len(camera_height_above_iPad_mm)):
        
        h = camera_height_above_iPad_mm[i]
        f = camera_focus_settings[i]
        print("h={0}mm, focus settings={1}".format(h,f))
    
        camera.change_focus(f)
        
        # Loop over all x-y positions
        for position_counter in range(n_robot_positions):
    
            aquisition_start_time = time.time()
            print("Taking images for x-y position {0} of {1}mm".format(position_counter,n_robot_positions))

            # Take a picture
            image_file_name_prefix = "h{0:02d}mm_pos{1:02d}".format(h,position_counter)
            camera.take_pic(image_file_name_prefix,file_directory=output_folder_path)
                
            t=time.time()
            print(t-aquisition_start_time)
        
            # Notify user 
            print("  Aquisition done, move to next x-y position")
        
            # Before moving to the next position, check how much time is left in order to synch with the robot
            aquisition_end_time = time.time()
            time_left = time_per_image_set_sec - (aquisition_end_time - aquisition_start_time)
            if time_left < 2:
                print("ERROR - ran out of time, please increase time_per_image_set_sec")
                return
            time.sleep(time_left)
        
    print("All Done")
    
if __name__ == "__main__":
    main()