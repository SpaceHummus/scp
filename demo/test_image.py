from PIL import Image

# function for image size in bites:

def is_Image_valid(filename):
    try :
        image_file = Image.open(filename)
        image_size = len(image_file.fp.read())
        print("File Size In Bytes:- ",image_size)
        return (image_size > 2000000)
    except :
        return False

print("is image small enough?", is_Image_valid("/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"))

# function for getting rgb for a pixel

def rgb_of_pixel(img_path, x, y):
    im = Image.open(img_path).convert('RGB')
    r, g, b = im.getpixel((x, y))
    a = (r, g, b)
    return a

img = "/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"
print ("rgb of pixel is:", rgb_of_pixel(img, 1, 1))

# function for getting image size in pixels

def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width*height
    

print ("image size in pixels:", get_num_pixels ("/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"))

#function for getting height & width

def image_width_height():
    filepath = "/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"
    img = Image.open(filepath)
    width,height = img.size
    return width, height

print("image width @ height:", image_width_height())

w,h = image_width_height()
for i in range(w):
    