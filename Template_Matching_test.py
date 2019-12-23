import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('red_potion_lower.jpg')
#img = cv2.imread('test.jpg')
img.astype(np.uint8)
img2 = img.copy()
template1 = cv2.cv2.imread('red_water_10.jpg')
template2 = cv2.cv2.imread('orange_potion_low.jpg')
#template2.astype(np.uint8)
#cv2.imwrite('res1.png',template)

h, w = template2.shape[0], template2.shape[1]

res_red = cv2.matchTemplate(img, template1, cv2.TM_CCOEFF_NORMED)
res_orange = cv2.matchTemplate(img, template2, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_red)
#min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res_orange)

top_left = max_loc
print(top_left)
print(max_val)
bottom_right = (top_left[0] + w, top_left[1] + h)

#cv2.rectangle(img,top_left, bottom_right, 255, 2)
#plt.subplot(121),plt.imshow(res,cmap = 'gray')
#plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(img,cmap = 'gray')
#plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
#plt.suptitle('cv2.TM_CCOEFF')
#plt.show()

threshold = 0.9
