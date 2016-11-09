import numpy
import cv2

img = cv2.imread('aklank.jpg' ,0)
cv2.imwrite('aklank.png' , img)
cv2.imshow('Original' , img)
cv2.waitKey(0)
cv2.destroyAllWindows()