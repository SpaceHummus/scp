# set of classes to support reading configuration data from logic_states.yaml
import logging


class SystemState:
    #illumination in next release 
    camera_configuration = None
    name = None
    def __init__(self,camera_configuration,name):
        self.camera_configuration = camera_configuration
        self.name = name
    def print_values(self):
        logging.info("System States values:")
        logging.info("name:%s", self.name)
        if self.camera_configuration != None:
            logging.info("image_frequency_min:%d",self.camera_configuration.image_frequency_min)
            logging.info("focus_position:")
            for fp in self.camera_configuration.focus_position:
                logging.info("* %d",fp)
            logging.info("exposure:%d",self.camera_configuration.exposure)
            logging.info("ISO:%d",self.camera_configuration.iso)
        else:
            logging.info("camera_configuration:None")

class CameraConfiguration:
    image_frequency_min = 5 # How often should we take images (minutes)
    exposure = 10
    iso = 10
    focus_position = []
    def __init__(self,image_frequency_min,exposure,iso,focus_position):
        self.image_frequency_min = image_frequency_min
        self.exposure = exposure
        self.iso = iso
        self.focus_position = focus_position

if __name__ == "__main__":
    s = SystemState(CameraConfiguration(6,20,30,[10,100,5]),"day_sun")    
    print(s.camera_configuration.iso)
    print(s.camera_configuration.focus_position)

    
