import numpy as np
import cv2

cap = cv2.VideoCapture(0) #Capture video from webcam (as argument passed is 0) Instead of video from webcam, pre-recorded video files
                          #can also be used.
frames = []     


#Below code takes 5 frames and take their median.
for _ in range(5):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(gray)

median = np.median(frames, axis=0).astype(dtype=np.uint8)
cv2.imshow('frame', median) 
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
