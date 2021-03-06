# set of classes to support reading configuration data from logic_states.yaml
import logging


class SystemState:
    camera_configuration = None
    illumination = None
    name = None
    def __init__(self,camera_configuration,illumination,name):
        self.camera_configuration = camera_configuration
        self.illumination = illumination
        self.name = name
    def print_values(self):
        logging.info("System States values:")
        logging.info("name:%s", self.name)
        if self.camera_configuration != None:
            logging.info("image_frequency_min:%d",self.camera_configuration.image_frequency_min)
            logging.info("root_image_frequency_min:%d",self.camera_configuration.root_image_frequency_min)
            logging.info("camera_A focus_position:")
            for fp in self.camera_configuration.focus_position["A"]:
                logging.info("* %d",fp)
            logging.info("camera_B focus_position:")
            for fp in self.camera_configuration.focus_position["B"]:
                logging.info("* %d",fp)
            logging.info("camera_C focus_position:")
            for fp in self.camera_configuration.focus_position["C"]:
                logging.info("* %d",fp)
            logging.info("camera_D focus_position:")
            for fp in self.camera_configuration.focus_position["D"]:
                logging.info("* %d",fp)
        else:
            logging.info("camera_configuration:None")
        if self.illumination != None:
            logging.info("R1:%d",self.illumination.group1_rgb.R)
            logging.info("G1:%d",self.illumination.group1_rgb.G)
            logging.info("B1:%d",self.illumination.group1_rgb.B)
            logging.info("R2:%d",self.illumination.group2_rgb.R)
            logging.info("G2:%d",self.illumination.group2_rgb.G)
            logging.info("B2:%d",self.illumination.group2_rgb.B)
            logging.info("far_red:%d",self.illumination.far_red)

class CameraConfiguration:
    image_frequency_min = 5 # How often should we take images (minutes)
    root_image_frequency_min = 60 # How often should we take images (minutes)    
    focus_position = {}
    def __init__(self,image_frequency_min, root_image_frequency_min,focus_position):
        self.image_frequency_min = image_frequency_min
        self.root_image_frequency_min = root_image_frequency_min
        self.focus_position = focus_position

class Illumination:
    group1_rgb = None
    group2_rgb = None
    far_red = 0
    def __init__(self,group1_rgb,group2_rgb,far_red):
        self.group1_rgb = group1_rgb
        self.group2_rgb = group2_rgb
        self.far_red = far_red

        
class RGB:
   R = 0
   G = 0
   B = 0
   def __init__(self,R,G,B):
       self.R = R
       self.G = G
       self.B = B

if __name__ == "__main__":
    s = SystemState(CameraConfiguration(6,20,30,[10,100,5]),"day_sun")    
    print(s.camera_configuration.focus_position)

    
