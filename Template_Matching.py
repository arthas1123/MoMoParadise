import cv2
import numpy as np
from matplotlib import pyplot as plt
from Control import LineageM_LD
from Module import ldconsole

#obj = LineageM_LD.LM(2, "./Data/Sample_img")
#obj.Keep_Emu_Img_Cap()

#img = cv2.imread('village.jpg')
img = cv2.imread('Emu_0_now.jpg')
img.astype(np.uint8)
img2 = img.copy()
template = cv2.cv2.imread('merchant_logo.jpg')
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

threshold = 0.9
loc = np.where( res >= threshold)
#print(len(loc))
#print(loc[0])
#print(loc[1])

for pt in zip(*loc[::-1]):
    #print(pt)
    cv2.rectangle(img, (pt[0] , pt[1]), (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv2.imwrite('res.png',img)

for pt in zip(*loc[::-1]):
    ldconsole.Dnconsole.touch(index = 0, x= pt[0], y=pt[1])