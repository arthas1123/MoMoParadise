from Module import adb
import cv2 as cv
from PIL import Image
import numpy as np
import pandas as pd

im = Image.open('menu_check.jpg') # Can be many different formats.

#menu_img = im.crop([0,889,363,1262])
menu_img = im.crop([889,0,1262,363])
menu_img.save('menu.jpg')
pic = np.array(menu_img)
#print(im.size)  # Get the width and hight of the image for iterating over
#print(pic[26,1246])  # Get the RGBA Value of the a pixel of an image
#print(pic[163,942])
#print(pic[305,1093])
#print(pic[659,294]) ### shopper blue
#print(pic)

r=0
g=1
b=2

r_query = 255
g_query = 41 
b_query = 42
loc = np.where((pic[:,:,r] == r_query))
y_loc = loc[0]
x_loc = loc[1]

mail_point = [203,306]
menu_point = [356,25]

print(menu_point[0] in x_loc)
print(menu_point[1] in y_loc)


#print(np.where((pic[:,:,r] == r_query) & (pic[:,:,g] == g_query) & (pic[:,:,b] == b_query)))

### Cnonvert RGB to HSV in opencv
#rgb_red = np.uint8([[[255,41,42]]])
#hsv_red = cv.cvtColor(rgb_red,cv.COLOR_RGB2HSV)
#print(hsv_red)


### Capture
#obj1 = adb.ADB(Device_Name="emulator-5554",Screen_Size=[1280,720])
#im1 = obj1.getWindow_Img_new(0)
#res = cv.imwrite('menu_check.jpg',im1)