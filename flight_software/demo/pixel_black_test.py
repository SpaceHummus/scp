import cv2
import numpy as np 
from matplotlib import pyplot as plt

# read image
img = cv2.imread('slice-309.png',0)
ret,thresh = cv2.threshold(img,0,230, cv2.THRESH_BINARY)
height, width = img.shape
print ("height and width : ",height, width)
size = img.size
print ("size of the image in number of pixels", size)

# plot the binary image
imgplot = plt.imshow(img, 'gray')
plt.show()

count = cv2.countNonZero(img)
print("number of black pixels:", img_size-count)

