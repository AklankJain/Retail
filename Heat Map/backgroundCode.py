import numpy as np
import cv2

cap = cv2.VideoCapture(0)
frames = []

for _ in range(5):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(gray)

median = np.median(frames, axis=0).astype(dtype=np.uint8)
cv2.imshow('frame', median)
cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()