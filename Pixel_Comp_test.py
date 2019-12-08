import cv2
import numpy as np

im1 = cv2.imread('test_full.jpg')
im2 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)
px_100 = im2[23,264]
px_90 = im2[23,245]
px_80 = im2[23,226]
px_70 = im2[23,207]

lower_red = np.array([0,43,46]) 
upper_red = np.array([10,255,255]) 

mask = cv2.inRange(im2, lower_red, upper_red)
# inrange return binary mask, ex:im1[y,x]
# Lineage M HP : Top-Left = [74,17], Bot-Right = [264,29]
# length = 190, width = 12
mask_crop = mask[17:29, 74:264]
result = cv2.bitwise_and(im1,im1,mask=mask)
#cv2.imshow('result',mask_crop)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

px_70_m= mask[23,207]



a = mask_crop[6,185]

print(px_70_m)