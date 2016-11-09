import argparse
import datetime
import imutils
import time
import cv2
import numpy as np 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# f1 = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# f2 = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
# f3 = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')
# f4 = cv2.CascadeClassifier('haarcascade_upperbody.xml')


 

cap = cv2.VideoCapture(0)
 
# initialize the first frame in the video stream
firstFrame = None

# videocapture = cv2.VideoCapture(0)
scale_factor= 1.05

while 1:
	ret, pic = cap.read()

	faces = face_cascade.detectMultiScale(pic, scale_factor , 5)
	# faces2 =  f1.detectMultiScale(pic , scale_factor , 5)
	# faces3 =   f2.detectMultiScale(pic , scale_factor , 5)
	# faces4  =   f3.detectMultiScale(pic , scale_factor , 5)


	for(x , y , w , h) in faces:
		cv2.rectangle(pic , (x,  y) , (x +w , y + h) , (255 , 255 , 0) , 2)
		#font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.putText(pic , 'Face' , (x , y) , font , 2 , (255 , 255 , 255) , 2 , cv2.LINE)

	
	print "Number of faces found {}".format(len(faces))
	cv2.imshow('face' , pic)
	#k = cv2.waitKey(0)
	
	key = cv2.waitKey(10)
	if key == 27:
		break
cv2.destroyAllWindows()	