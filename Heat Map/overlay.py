# import the necessary packages

import numpy as np
import cv2

# load the image
image = cv2.imread("Resized_trijal.png")
print image.shape

im1 = cv2.imread('sky_main.jpg')
print im1.shape

im1= cv2.resize(im1, (700, 700))

for i in range(500,700):
    for j in range (500,700):
        im1[i,j]=(255,255,255)



alpha=0.7
# loop over the alpha transparency values
#for alpha in np.arange(0, 1.1, 0.1)[::-1]:
# create two copies of the original image -- one for
# the overlay and one for the final output image
overlay = image.copy()
output = image.copy()

dest=im1.copy()

# draw a red rectangle surrounding Adrian in the image
# along with the text "PyImageSearch" at the top-left
# corner
#cv2.rectangle(overlay, (420, 205), (595, 385),(0, 0, 255), -1)

# apply the overlay
cv2.addWeighted(overlay, alpha,dest , 1 - alpha,0, output)

# show the output image
print("alpha={}, beta={}".format(alpha, 1 - alpha))
cv2.imshow("Output", output)
cv2.waitKey(0)