import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('red_potion_lower.jpg')
#img = cv2.imread('test.jpg')
img.astype(np.uint8)
img2 = img.copy()
template = cv2.cv2.imread('red_water_10.jpg')
template.astype(np.uint8)
#cv2.imwrite('res1.png',template)

h, w = template.shape[0], template.shape[1]

res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img,top_left, bottom_right, 255, 2)
plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle('cv2.TM_CCOEFF')
#plt.show()

threshold = 0.8
loc = np.where( res >= threshold)
print(len(loc))
print(loc[0])
print(loc[1])
print(res[602][925])
for pt in zip(*loc[::-1]):
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.imwrite('res.png',img)