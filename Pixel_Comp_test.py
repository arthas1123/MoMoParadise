import cv2
import numpy as np

im1 = cv2.imread('test_full.jpg')
im2 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)
px_100 = im2[264,23]
px_90 = im2[245,23]
px_80 = im2[226,23]
px_70 = im2[207,23]

lower_red = np.array([0,43,46]) 
upper_red = np.array([10,255,255]) 

mask = cv2.inRange(im2, lower_red, upper_red)
result = cv2.bitwise_and(im1,im1,mask=mask)
#cv2.imshow('result',result)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

print(result[245,23])

#print(px_80_m)