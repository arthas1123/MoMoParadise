import cv2
import numpy as np

im1 = cv2.imread('village.jpg')
#im1 = cv2.imread('test3.jpg')
im2 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)
px_100 = im2[23,264]
px_90 = im2[23,245]
px_80 = im2[23,226]
px_70 = im2[23,207]

# lower mask (0-10)
lower_red = np.array([0,50,120])
upper_red = np.array([10,255,255])
mask0 = cv2.inRange(im2, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([170,50,120])
upper_red = np.array([180,255,255])
mask1 = cv2.inRange(im2, lower_red, upper_red)

# join my masks
mask = mask0+mask1

# Blue Mask
lower_blue = np.array([90,30,130]) 
upper_blue = np.array([110,80,255])
blue_mask = cv2.inRange(im2, lower_blue, upper_blue)

# Green Mask
lower_green = np.array([50,43,46]) 
upper_green = np.array([70,255,255])
green_mask = cv2.inRange(im2, lower_green, upper_green)

# inrange return binary mask, ex:im1[y,x]
# Lineage M HP : Top-Left = [74,17], Bot-Right = [264,29]
# length = 190, width = 12
#mask_crop = mask[17:29, 74:264]
#mask_crop = green_mask[17:29, 74:264]

result = cv2.bitwise_and(im1,im1,mask=blue_mask)
cv2.imshow('result',result)
cv2.waitKey(0)
cv2.destroyAllWindows()

px_70_m= mask[23,207]



a = mask_crop[6,185]

print(px_70_m)