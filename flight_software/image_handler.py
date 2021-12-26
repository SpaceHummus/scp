import logging
from PIL import Image

# function for image size in bites:

MIN_IMAGE_SIZE = 2000000 # 2GB
SKIP_PIXELS = 40

def check_img_size(img):
    try :
        image_size = len(img.fp.read())
        logging.debug("File Size In Bytes:%d",image_size)
        return (image_size > MIN_IMAGE_SIZE)
    except :
        return False


# function for getting rgb for a pixel
def rgb_of_pixel(img_rgb, x, y):
    r, g, b = img_rgb.getpixel((x, y))
    a = (r, g, b)
    return a


# function for getting image size in pixels
def get_num_pixels(img):
    width, height = img.size
    return width*height
    

#function for getting height & width
def image_width_height(img):
    width,height = img.size
    return width, height

#print("image width @ height:", image_width_height())
def check_black_pixels(img):
    im_rgb = img.convert('RGB')
    w,h = image_width_height(img)
    count_black = 0
    for y in range(0,h,SKIP_PIXELS):
        for x in range(0,w,SKIP_PIXELS):
            a = rgb_of_pixel(im_rgb, x, y)
            #print(a)
            if (a[0]<=50 and a[1]<=50 or a[0]<=50 and a[2]<=50 or a[1]<=50 and a[2]<=50):
                count_black +=1
    logging.debug("number of balcks = %d",count_black)
    logging.debug("number of non balcks = %d",(w*h) - count_black)
    logging.debug("total of pixels = %d",(w*h))
    percentage_of_balcks = (count_black/(w*h))*100
    logging.debug("percentage_of_balcks:%d", percentage_of_balcks)
    
    if percentage_of_balcks > 80 : 
        return False
    else :
        return True

# run alll image chekcs (size + black pixels)
def check_image(img_path):
    try:
        img = Image.open(img_path)
        if not check_img_size(img):
            logging.error("is image small:%s",img_path)
        if not check_black_pixels(img):
            logging.error("image is too dark:%s",img_path)
    except:
        logging.error("Unable to open image:%s",img_path)
    
if __name__ == "__main__":
    print(check_image("/home/pi/dev/flight-software/images/21-10-17__13_49_CD_F0512.jpg"))