import numpy as np
import cv2
import csv

f = open('datapoints.csv', 'wt')
writer = csv.writer(f)
def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        writer.writerow((x+pad_w, y+pad_h, x+w-pad_w, y+h-pad_h))
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


if __name__ == '__main__':

    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
    cap=cv2.VideoCapture('video1.mp4')
    frame_now = cap.read()[1]
    frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
    cv2.imwrite('firstFrameGrayHog.png', frame_now)
    while True:
        _,frame=cap.read()
       # cv2.line(frame, (250,0), (250, 725), (255, 0, 0), 1)
       # cv2.line(frame, (1000,0), (1000, 725), (0, 0, 255), 1)
        found, w=hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
        draw_detections(frame,found)
        cv2.imshow('feed',frame)
        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            f.close()
            break
    cv2.destroyAllWindows()