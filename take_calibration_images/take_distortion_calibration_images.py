
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
from PIL import Image

# General configuration of this script, these numbers should match .gcode
#########################################################################

# Number of x-y robot positions
n_robot_positions = 49

# Z positions & camera focus positions (for each height one focus position)
camera_height_above_iPad_mm = [90,  70,  60,  50,  43]
# Comment below if you would like to use focus setting to verify for each height what focus setting to use
# camera_focus_settings =       [110, 150, 190, 210, 230] 

# Time it takes to complete image aquisition for each x-y position
time_per_image_set_sec = 30

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

    # Get input from user about the camera we will use today
    print("What is the camera serial number we will calibrate today (Example: C01)?")
    camera_sn = input("")
    camera_sn = camera_sn.upper()
    print("Selected '{0}'".format(camera_sn))
    time.sleep(1)
    
    camera = camera_handler.CameraHandler(camera_id=camera_sn)
    camera.change_active_camera('A')
    
    # Create output folder
    output_folder_path = "{0}_distortion_calibration_images_{1}/".format(camera_sn,time.strftime("%Y-%m-%d"))
    create_image_folder_if_not_exist(output_folder_path)
    
    # Ask user to start robot
    print("")
    print("Make shure the robot is centered at the pattern")
    print("On Rotric's consule run take_distortion_calibration_images.gcode")
    val = input("Press Enter when robot is finished moving to the center position")
    time.sleep(2) # Add a delay to let system stabilize
    
    # Loop over all heights
    image_counter = 0
    for i in range(len(camera_height_above_iPad_mm)):
        
        h = camera_height_above_iPad_mm[i]
        f = camera.change_focus_to_h(h)
        # camera.change_focus(f) # Directly control focus
        print("h={0}mm, focus settings={1}".format(h,f))
        
        # Loop over all x-y positions
        for position_counter in range(n_robot_positions):
            
            pos = position_counter
            if (i % 2) == 1: 
                # Positions are flipped, start from the end
                pos = n_robot_positions-position_counter-1
    
            aquisition_start_time = time.time()
            print("Taking images for x-y position {0} of {1}mm".format(pos,n_robot_positions))
            
            # Take a sample picture (robot might be still moving
            tmp_file_path, _ = camera.take_pic("tmp")

            # Take a picture
            image_file_name_prefix = "img{0:03d}_h{1:02d}mm_pos{2:02d}".format(image_counter,h,pos)
            img_file_path, _ = camera.take_pic(image_file_name_prefix,file_directory=output_folder_path)
            image_counter = image_counter + 1
            
            # Compare the two images taken, if they are different arm was still moving while the first image was taken and need to be re-done
            tmp_img = np.array(Image.open(tmp_file_path)) # Read image
            img = np.array(Image.open(img_file_path)) # Read image
            tmp_img = np.mean(tmp_img, 2, np.float32)# Convert to RGB
            img = np.mean(img, 2, np.float32)# Convert to RGB
            img_diff = np.abs(tmp_img-img) # Compute the difference
            if np.count_nonzero(img_diff>50) > 20: 
                # Some pixels are meaningfully different, we need to add a short delay to make sure camera is not moving
                print("Meaningful difference, we need to add time to timer")
                is_burn_more_time = True
            else:
                is_burn_more_time = False
                
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
            
            if is_burn_more_time:
                time.sleep(5) # Sleep for x seconds
        
    print("All Done")
    
if __name__ == "__main__":
    main()