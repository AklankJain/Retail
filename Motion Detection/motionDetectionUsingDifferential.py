import cv2
import sys
import time
import csv
import numpy


BLUR_SIZE = 3
NOISE_CUTOFF =10


cam = cv2.VideoCapture('tvf3.dav')

#cam.set(3, 640)
#cam.set(4, 480)

currList=[]
prevLIst=[]
uniqueList=[]

moveTime=0
stillTime=0

cam.set(cv2.cv.CV_CAP_PROP_FPS, 1) #this doesn't work
fps=cam.get(cv2.cv.CV_CAP_PROP_FPS)
print "Current FPS: ",fps

f=open('co-ordinates.csv','wt')
g=open('dataPoints.csv','wt')
h=open('dataPoints1.csv','wt')
writer=csv.writer(f)
writer1=csv.writer(g)
writer2=csv.writer(h)
window_name = "delta view"
cv2.namedWindow(window_name, cv2.CV_WINDOW_AUTOSIZE)
window_name_now = "now view"
cv2.namedWindow(window_name_now, cv2.CV_WINDOW_AUTOSIZE)

# Stabilize the detector by letting the camera warm up and
# seeding the first frames.
frame_now = cam.read()[1]
frame_now = cam.read()[1]
frame_now = cv2.cvtColor(frame_now, cv2.COLOR_RGB2GRAY)



#in case of showroom use this code
im_temp=cv2.imread('frameToCopyFrom.png')
cv2.imwrite('firstFrameGray.png',im_temp)

#else normally us this
#cv2.imwrite('firstFrameGray.png',frame_now)

frame_now = cv2.blur(frame_now, (BLUR_SIZE, BLUR_SIZE))
frame_prior = frame_now

delta_count_last = 1

print frame_now.shape

width,height=frame_now.shape

people_going_up = 0
people_going_down = 0


pGoingUp=[]
pGoingDown=[]

customerCount=1

#fl=0
timeFlag=0
while True:

    #cv2.waitKey(int(1 / fps * 1000))


    #cv2.line(frame_now,(0,height/2),(width,height/2),(255,0,0),3)
    frame_delta = cv2.absdiff(frame_prior, frame_now)

    frame_delta = cv2.GaussianBlur(frame_delta, (11, 11), 0)
    frame_delta = cv2.threshold(frame_delta, NOISE_CUTOFF, 255, cv2.THRESH_BINARY)[1]

    delta_count = cv2.countNonZero(frame_delta)

    #cv2.line(frame_now,(0,height/2),(width,height/2),(255,0,0),1)
    # Visual detection statistics output.
    # Normalize improves brightness and contrast.
    # Mirror view makes self display more intuitive.
    cv2.normalize(frame_delta, frame_delta, 0, 255, cv2.NORM_MINMAX)
    frame_delta = cv2.flip(frame_delta, 1)
    frame_delta= cv2.flip(frame_delta,1)


    #cv2.putText(frame_delta, "DELTA: %d" % (delta_count),(5, 15), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 255, 255))

    # **********Draw a bounding box:*************************************************


    # frameDelta = cv2.absdiff(frame_now, frame_prior)
    #thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = frame_delta
    thresh = cv2.dilate(thresh, None, iterations=2)
    kernal = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    thresh = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernal)
    frame_delta=thresh


    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image


    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                 cv2.CHAIN_APPROX_NONE)
    #print cnts

    i = 0
    # loop over the contours
    # for c in cnts:
    # if the contour is too small, ignore it
    # if cv2.contourArea(c) >10:
    # cv2.drawContours(frame_delta , cnts , -1 , (255 , 255 , 0) , 3)

    flag = 0
    contourDetected=0
    for c in cnts:
        if cv2.contourArea(c)>1000:
            ################################################# timeFlag=1
            contourDetected=contourDetected+1
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            M = cv2.moments(c)
            if M['m00']!=0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                #writer.writerow((cx, cy))
            #print cx,cy

            #img1 = cv2.imread('firstFrame.png')
            #height,width,channel=img1.shape



            cv2.rectangle(frame_delta, (x, y), (x + w, y + h), (255, 255, 0), 2)
            writer.writerow((x,y,w,h,cx,cy))
            #currList.append((cx, cy))
            perimeter = cv2.arcLength(c,True)
            currList.append(perimeter)


    #********************************************************************************
    #Counter*************************************************

    if contourDetected>0:
        uflag=0
        if len(currList)>=1 and len(prevLIst)>0:
            for i in range(0,len(currList)):
                for j in range(0,len(prevLIst)):
                    if currList[i]==prevLIst[j]:
                        if len(uniqueList)==0:
                            uniqueList.append(currList[i])
                            name='customer '+str(customerCount)
                            writer2.writerow((name,customerCount,150,abs(moveTime-stillTime)))
                            writer1.writerow((150, moveTime - stillTime))
                            customerCount = customerCount + 1
                        else:
                            for k in range(0,len(uniqueList)):
                                if uniqueList[k]==currList[i]:
                                    uflag=1
                            if uflag==0:
                                uniqueList.append(currList[i])
                                name = 'customer ' + str(customerCount)
                                writer2.writerow((name, customerCount, 150,abs(moveTime-stillTime)))
                                writer1.writerow((150, moveTime - stillTime))
                                customerCount = customerCount + 1



    prevLIst=currList
    currList[:]=[]
    contourDetected=0


    #********************************************************

    cv2.imshow(window_name, frame_delta)

    # frame_delta = cv2.threshold(frame_delta, 92, 255, 0)[1]
    dst = cv2.flip(frame_now, 1)
    dst = cv2.flip(dst, 1)
    dst = cv2.addWeighted(dst, 1.0, frame_delta, 0.9, 0)
    cv2.imshow(window_name_now, dst)

    # Stdout output.
    # Only output when there is new movement or when movement stops.
    # Time codes are in epoch time format.
    if (delta_count_last == 0 and delta_count != 0 ):
        moveTime=time.time()

        sys.stdout.write("MOVEMENT %f\n" % time.time())
        sys.stdout.flush()
    elif delta_count_last != 0 and delta_count == 0:
        stillTime=time.time()

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
        print "Number of unique contours: ",len(uniqueList)
        #print "people going up: ",people_going_up
        #print "people going down: ",people_going_down
        break
