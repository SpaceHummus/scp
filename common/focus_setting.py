import logging
import yaml
import glob
import numpy as np

# This class reads focus setting yaml and supports converting focus distance to focus setting for each camera
class FocusSetting:

    focus_setting = None
 
    # Camera id can be "C01", "C02" etc.
    def __init__(self, camera_id=""):
        
        # Search for camera setting yaml
        match_file_paths = glob.glob("{0}_focus_setting_*.yaml".format(camera_id))
        if len(match_file_paths) == 0:
            logging.error("Cannot find any camera id: {0}_focus_setting_*.yaml".format(camera_id))
            return
        
        # Load information from yaml
        file = open(match_file_paths[0],"r")
        self.focus_setting = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        
        logging.info(
            "Loaded focus setting for camera id {0} aquired at {1}".format(
            self.focus_setting["camera_id"],self.focus_setting["calibration_date"]))
        
    # Change camera focus to a specific height
    # INPUTS:
    #   height_mm - height in mm to set focus to
    # OUTPUTS:
    #   returns focus setting
    def focus_distance_to_setting(self, height_mm):
        
        # Check focus_setting exists
        if self.focus_setting == None:
            logging.error("No focus setting, please specify camera id on class constractor")
            return
        
        # Using interpolation, figure out what is the recommended focus value
        focus = np.interp(height_mm,self.focus_setting["height_mm"],self.focus_setting["focus_setting"])
        focus = int(focus) # Make sure this is a round number
        
        return focus
    

if __name__ == "__main__":
    fs = FocusSetting("C02")
    
    tmp = fs.focus_distance_to_setting(100)