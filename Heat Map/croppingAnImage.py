import cv2
import numpy as np

img = cv2.imread('1.jpg')
cv2.imshow("original Image",img)
height,width,channels=img.shape
print height,width,channels
crop_img = img[200:210, 100:110] # Crop from x, y, w, h -> 100, 200, 300, 400
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

crop_img=cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
cv2.imshow("cropped", crop_img)
height,width=crop_img.shape
print crop_img[5,5]


#**SELF REMINDER: IF NEEDED PUT THE CODE TO SAVE CROPPED IMAGE TO EXTERNAL FILE TOO**
cv2.waitKey(0)
