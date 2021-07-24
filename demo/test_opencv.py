import cv2
import os

# cam_idex=[0,4,8,19]
cam_idex=[19]

for i in cam_idex:
    print("taking picture from cam:",i)
    exec_str = "fswebcam -d /dev/video%d -r 1088x1080 --no-banner image%d.jpg" %(i,i)
    print(exec_str)
    os.system(exec_str)
    # videoCaptureObject = cv2.VideoCapture(i)
    # ret,frame = videoCaptureObject.read()
    # cv2.imwrite("NewPicture%d.jpg"%i,frame)
    # videoCaptureObject.release()
