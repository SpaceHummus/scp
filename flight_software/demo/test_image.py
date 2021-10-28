from PIL import Image

# function for image size in bites:

def is_Image_valid(img_link):
    try :
        image_file = Image.open(img_link)
        image_size = len(image_file.fp.read())
        print("File Size In Bytes:- ",image_size)
        return (image_size > 2000000)
    except :
        return False

#print("is image big enough?", is_Image_valid(img_link))

# function for getting rgb for a pixel

def rgb_of_pixel(img_rgb, x, y):
    r, g, b = img_rgb.getpixel((x, y))
    a = (r, g, b)
    return a

#img = "/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"
#print ("rgb of pixel is:", rgb_of_pixel(img, 1, 1))

# function for getting image size in pixels

def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    return width*height
    

#print ("image size in pixels:", get_num_pixels ("/home/pi/dev/flight-software/images/21-10-07__09_51_CA_F0260.jpg"))

#function for getting height & width

def image_width_height(img_link):
    filepath = img_link
    img = Image.open(filepath)
    width,height = img.size
    return width, height

#print("image width @ height:", image_width_height())

def check_image(img_link):
    res = is_Image_valid(img_link)
    if (not res):
        print("is image big enough")
        return False

    #print("is image big enough?", is_Image_valid(img_link))
    im_rgb = Image.open(img_link).convert('RGB')
    w,h = image_width_height(img_link)
    count_black = 0
    for y in range(h):
        for x in range(w):
            a = rgb_of_pixel(im_rgb, x, y)
            #print(a)
            if (a[0]<=50 and a[1]<=50 or a[0]<=50 and a[2]<=50 or a[1]<=50 and a[2]<=50):
                count_black +=1
    print("number of balcks = ",count_black)
    print("number of non balcks = ",(w*h) - count_black)
    print("total of pixels = ",(w*h))
    percentage_of_balcks = (count_black/(w*h))*100
    print("percentage_of_balcks:", percentage_of_balcks)
    
    return not(percentage_of_balcks > 80)
    
print(check_image("/home/pi/dev/flight-software/images/21-10-17__13_49_CD_F0512.jpg"))