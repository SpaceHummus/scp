from camera_handler import CameraHandler
from PIL import Image

# a script to take pictures in all cameras in a range of focus values

f_start = 10
f_end = 1000
f_step = 10

camera = CameraHandler()

def crop_image(image_path):
    # Opens a image in RGB mode
    im = Image.open(image_path)
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size
    
    # Setting the points for cropped image
    left = width * 0.4
    top = height * 0.4
    right = width * 0.8
    bottom = height * 0.8
    
    # Cropped image of above dimension
    # (It will not change original image)
    im = im.crop((left, top, right, bottom))
    im.save(image_path)    

def take_pictures(camera_id):
    camera.change_active_camera(camera_id)
    for f in range(f_start,f_end,f_step):
        camera.change_focus(f)
        print(f"taking image. camera:{camera_id} focus:{f}")
        camera.take_pic("focus_test")

crop_image("/home/pi/dev/scp/flight_software/images/22-02-02__02_53_CC_F0220.jpg")
# take_pictures("A")
# take_pictures("B")
# take_pictures("C")
# take_pictures("D")



