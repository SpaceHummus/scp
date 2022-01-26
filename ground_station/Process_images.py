# import download_images.py
import os
import cv2
import datetime
import shutil
import FocusStack
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# C:\Users\GAL\Desktop\Space_Hummus\Images\cycle1\

def stackHDRs(image_files, images_dir):
    focusimages = []
    for img in image_files:
        print("Reading in file {}".format(img))
        focusimages.append(cv2.imread(images_dir + "/{}".format(img)))

    merged = FocusStack.focus_stack(focusimages)
    cv2.imwrite("merged.png", merged)


def focus_staking(my_dir):
    merged_dir = os.path.join(my_dir, "Merged_images")
    try:
        os.mkdir(merged_dir)
    except:
        print("Folder 'Merged_images' already exists")
    try:
        process_dir = os.path.join(my_dir, "process")
        os.mkdir(process_dir)
    except:
        print("Folder 'process' already exists")

    dir_list = os.listdir(my_dir)
    n_img = len(dir_list)
    while n_img > 2:
        print("Working on", n_img-2, "images")

        img1_name = dir_list[0]
        img1_prefix = img1_name[0:18]
        print(img1_prefix)
        shutil.move(my_dir + img1_name, my_dir + "process/" + img1_name)
        for n2 in range(1, n_img): # n=n1+1 till (n_img-1)
            img2_name = dir_list[n2]
            img2_prefix = img2_name[0:18]
            if (img1_prefix == img2_prefix) or (img1_prefix[0:13] == img2_prefix[0:13] and img1_prefix[16:18] == img2_prefix[16:18] and abs(int(img1_prefix[13:15])-int(img2_prefix[13:15])) <= 1):
                shutil.move(my_dir + img2_name, my_dir + "process/" + img2_name)
        image_files = sorted(os.listdir(my_dir + "process/"))
        print("Focus stacking images in: ", my_dir + "process/")
        print(image_files)
        stackHDRs(image_files, my_dir + "process")
        # input("Just checking - merged image was created")

        for filename in os.listdir(my_dir + "process/"):
            try:
                os.remove(my_dir + "process/" + filename)
            except:
                print("Couldn't delete process dir contenet")
        shutil.move("merged.png", my_dir + "/Merged_images/" + img1_prefix + "_focus_stacked.png")
        # input("Just checking - merged image was copied and process folder deleted")
        dir_list = os.listdir(my_dir)
        n_img = len(dir_list)

def Video_writer(image_folder, video_folder, camera, start_time):
    images = []
    for img in os.listdir(image_folder):
        if img.endswith(".png") and img.__contains__(camera):

            # Calc the time passed from eperiment start time
            image_date = datetime.datetime(int(img[0:2])+2000, int(img[3:5]), int(img[6:8]), int(img[10:12]), int(img[13:15]), 0)
            delta_time = image_date - start_date

            # Write the time passed on the mage
            img_with_text= Image.open(image_folder + "/" + img) # Open an Image
            I1 = ImageDraw.Draw(img_with_text) # Call draw Method to add 2D graphics in an image
            I1.text((28, 36), str(delta_time), font=ImageFont.truetype('arial.ttf', 90), fill=(255, 240, 0)) # Add Text to an image
            img_with_text.save(image_folder + '/' + img) # Save the edited image

            images.append(img)

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    image_1=images[0]
    image_last=images[len(images)-1]
    video_name = video_folder + "Hummus_growth_" + image_1[0:15] + "_till_" + image_last[0:15] + "_" + camera + ".avi"
    print(video_name)
    fps = 2 # frame per second
    video = cv2.VideoWriter(video_name, 0, fps, (width, height))

    for image in images:
        print(os.path.join(image_folder, image))
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


# run in terminal: python download_images.py 1z6weX9LhJIZ8iZd_F1t-uAKWvTeuineh 21-08-17__05_06 21-08-17__06_51 A,C 110,150,190,210,230 C:\Users\GAL\Desktop\Space_Hummus\Images\cycle1

my_dir = "C:/Users/GAL/Desktop/Space_Hummus/Images/cycle1/" # input('enter dir  ')
print(my_dir)
print(my_dir + "Merged_images")
#focus_staking(my_dir)
video_folder = my_dir
start_time = "21-08-17__05_00"
# example: datetime.datetime(2017, 6, 21, 18, 25, 30)
start_date = datetime.datetime(int(start_time[0:2])+2000, int(start_time[3:5]), int(start_time[6:8]), int(start_time[10:12]), int(start_time[13:15]), 0)
Video_writer(my_dir + "Merged_images", video_folder, "CA", start_date)
Video_writer(my_dir + "Merged_images", video_folder, "CC", start_date)