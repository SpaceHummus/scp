# set of classes to support reading configuration data from logic_states.yaml

class SystemState:
    #illumination in next release 
    camera_configuration = None
    name = None
    def __init__(self,camera_configuration,name):
        self.camera_configuration = camera_configuration
        self.name = name
    def print_values(self):
        print("name:", self.name)
        print("image_frequency_min:",self.camera_configuration.image_frequency_min)
        print("focus_position:")
        print("\tmin:",self.camera_configuration.focus_position.min)
        print("\tmax:",self.camera_configuration.focus_position.max)
        print("\tstep:",self.camera_configuration.focus_position.step)
        print("exposure:",self.camera_configuration.exposure)
        print("ISO:",self.camera_configuration.iso)

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

    
