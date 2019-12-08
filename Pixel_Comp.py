import cv2
import numpy as np

# Lineage M HP : Top-Left = [74,17], Bot-Right = [264,29]
# length = 190, width = 12
# 90% = 74 + 190 * 0.9 => [245,23]
# 80% => [226, 23]
# 70% => [207, 23]
# 60% => [188, 23]
# 50% => [169, 23]
# 40% => [150, 23]


# test3 ==> 216, above 70 lower than 80
# test4 ==> 185, 50~60
im1 = cv2.imread('mask.jpg')
im2 = cv2.cvtColor(im1,cv2.COLOR_BGR2HSV)
px_100 = im2[264,23]
px_90 = im2[245,23]
px_80 = im2[226,23]
px_70 = im2[207,23]

print(np.all(im1 == 0))


# BGR color 
s100 = np.array([81,103,120])
s90 = np.array([156,172,181])
s80 = np.array([89,190,226])
s70 = np.array([76,97,111])

# HSV_RED:
lower_red = np.array([0,43,46]) 
upper_red = np.array([10,255,255]) 
#mask = cv2.inRange(im2, lower_red, upper_red) 
#cv2.imshow('im2',mask)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#print(s80[2])



#[200,25]
print(px_100,px_90,px_80,px_70)



#use opencv to capture pixels and set a certain threshold