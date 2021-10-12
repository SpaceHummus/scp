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
            logging.info("focus_position:")
            for fp in self.camera_configuration.focus_position:
                logging.info("* %d",fp)
            logging.info("exposure:%d",self.camera_configuration.exposure)
            logging.info("ISO:%d",self.camera_configuration.iso)
        else:
            logging.info("camera_configuration:None")
        if self.illumination != None:
            logging.info("R:%d",self.illumination.R)
            logging.info("G:%d",self.illumination.G)
            logging.info("B:%d",self.illumination.B)
            logging.info("number_of_leds:%d",self.illumination.number_of_leds)
            logging.info("far_red:%d",self.illumination.far_red)

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

class Illumination:
    R = 0
    G = 0
    B = 0
    number_of_leds = 0
    far_red = 0
    def __init__(self,R,G,B,number_of_leds,far_red):
        self.R = R
        self.G = G
        self.B = B
        self.number_of_leds = number_of_leds
        self.far_red = far_red

if __name__ == "__main__":
    s = SystemState(CameraConfiguration(6,20,30,[10,100,5]),"day_sun")    
    print(s.camera_configuration.iso)
    print(s.camera_configuration.focus_position)

    
