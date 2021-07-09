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
        logging.info("*** name:%s ***", self.name)
        logging.info("image_frequency_min:%d",self.camera_configuration.image_frequency_min)
        logging.info("focus_position:")
        logging.info("\tmin:%d",self.camera_configuration.focus_position.min)
        logging.info("\tmax:%d",self.camera_configuration.focus_position.max)
        logging.info("\tstep:%d",self.camera_configuration.focus_position.step)
        logging.info("exposure:%d",self.camera_configuration.exposure)
        logging.info("ISO:%d",self.camera_configuration.iso)

class CameraConfiguration:
    image_frequency_min = 5 # How often should we take images (minutes)
    exposure = 10
    iso = 10
    focus_position = None
    def __init__(self,image_frequency_min,exposure,iso,focus_position):
        self.image_frequency_min = image_frequency_min
        self.exposure = exposure
        self.iso = iso
        self.focus_position = focus_position

class FocusPosition:
    min=0
    max=1023
    step=100
    def __init__(self,min,max,step):
        self.min = min
        self.max = max
        self.step = step

if __name__ == "__main__":
    s = SystemState(CameraConfiguration(6,20,30,FocusPosition(10,100,5)))    
    print(s.camera_configuration.iso)
    print(s.camera_configuration.focus_position.step)

    
