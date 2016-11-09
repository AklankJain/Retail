import cv2
import sys
import time
import csv
import numpy

# The two main parameters that affect movement detection sensitivity
# are BLUR_SIZE and NOISE_CUTOFF. Both have little direct effect on
# CPU usage. In theory a smaller BLUR_SIZE should use less CPU, but
# for the range of values that are effective the difference is
# negligible. The default values are effective with on most light
# conditions with the cameras I have tested. At these levels the
# detectory can easily trigger on eye blinks, yet not trigger if the
# subject remains still without blinking. These levels will likely be
# useless outdoors.
BLUR_SIZE = 3
NOISE_CUTOFF = 12
# Ah, but the third main parameter that affects movement detection
# sensitivity is the time between frames. I like about 10 frames per
# second. Even 4 FPS is fine.
# FRAMES_PER_SECOND = 10

cam = cv2.VideoCapture('video1.mp4')
# 320*240 = 76800 pixels
# cam.set(3, 320)
# cam.set(4, 240)
# 640*480 = 307200 pixels
cam.set(3, 640)
cam.set(4, 480)

cam.set(cv2.cv.CV_CAP_PROP_FPS, 1)
fps=cam.get(cv2.cv.CV_CAP_PROP_FPS)
print "Current FPS: ",fps

f=open('co-ordinates.csv','wt')
writer=csv.writer(f)

window_name = "delta view"
cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
window_name_now = "now view"
cv2.namedWindow(window_name_now, cv2.CV_WINDOW_AUTOSIZE)

# Stabilize the detector by letting the camera warm up and
# seeding the first frames.
frame_now = cam.read()[1]
frame_now = cam.read()[1]
frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
cv2.imwrite('firstFrameGray.png',frame_now)
frame_now = cv2.blur(frame_now, (BLUR_SIZE, BLUR_SIZE))
frame_prior = frame_now

delta_count_last = 1


while True:
    frame_delta = cv2.absdiff(frame_prior, frame_now)
    frame_delta = cv2.threshold(frame_delta, NOISE_CUTOFF, 255, 3)[1]
    delta_count = cv2.countNonZero(frame_delta)

    # Visual detection statistics output.
    # Normalize improves brightness and contrast.
    # Mirror view makes self display more intuitive.
    cv2.normalize(frame_delta, frame_delta, 0, 255, cv2.NORM_MINMAX)
    frame_delta = cv2.flip(frame_delta, 1)
    frame_delta= cv2.flip(frame_delta,1)

    #cv2.putText(frame_delta, "DELTA: %d" % (delta_count),(5, 15), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))

    # **********Draw a bounding box:*************************************************




    # frameDelta = cv2.absdiff(frame_now, frame_prior)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_NONE)
    # print cnts

    i = 0
    # loop over the contours
    # for c in cnts:
    # if the contour is too small, ignore it
    # if cv2.contourArea(c) >10:
    # cv2.drawContours(frame_delta , cnts , -1 , (255 , 255 , 0) , 3)
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        #img1 = cv2.imread('firstFrame.png')
        #height,width,channel=img1.shape
        if area > 4000:
            cv2.rectangle(frame_delta, (x, y), (x + w, y + h), (255, 255, 0), 2)
            writer.writerow((x,y,w,h))


            img1=cv2.imread('firstFrame.png')
            #cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 255, 0), -1)
            #cv2.imwrite('firstSS.png',img1)
            #print "shape1: ",img1.shape


            #img2=cv2.imwrite('framePP.png',frame_delta)
            #img2=cv2.imread('framePP.png')
            #print "shape2: ",img2.shape



            # continue

            #     # compute the bounding box for the contour, draw it on the frame,
            #     # and update the text
            #     (x, y, w, h) = cv2.boundingRect(c)
            #     cv2.rectangle(frame_now, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #********************************************************************************

    cv2.imshow(window_name, frame_delta)

    # frame_delta = cv2.threshold(frame_delta, 92, 255, 0)[1]
    dst = cv2.flip(frame_now, 1)
    dst = cv2.flip(dst, 1)
    dst = cv2.addWeighted(dst, 1.0, frame_delta, 0.9, 0)
    cv2.imshow(window_name_now, dst)

    # Stdout output.
    # Only output when there is new movement or when movement stops.
    # Time codes are in epoch time format.
    if (delta_count_last == 0 and delta_count != 0):
        sys.stdout.write("MOVEMENT %f\n" % time.time())
        sys.stdout.flush()
    elif delta_count_last != 0 and delta_count == 0:
        sys.stdout.write("STILL    %f\n" % time.time())
        sys.stdout.flush()
    delta_count_last = delta_count

    # Advance the frames.
    frame_prior = frame_now

    frame_now = cam.read()[1]

    frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)
    frame_now = cv2.blur(frame_now, (BLUR_SIZE, BLUR_SIZE))
    # Wait up to 10ms for a key press. Quit if the key is either ESC or 'q'.
    key = cv2.waitKey(10)
    if key == 0x1b or key == ord('q'):
        cv2.destroyWindow(window_name)
        f.close()
        break
