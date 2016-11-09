import numpy as np
import cv2

data = np.loadtxt('co-ordinates.csv', delimiter=',')
#data = np.loadtxt('datapoints.csv', delimiter=',')

# Putting data from csv file to variables
x = data[:, 0]
y = data[:, 1]
w = data[:, 2]
h = data[:, 3]

# Taking out size of the file
k = x.shape[0]

# Converting npArray to simple array
np.asarray(x)
np.asarray(y)
np.asarray(w)
np.asarray(h)

# Reading image
img1 = cv2.imread('firstFrameGray.png')
#img1 = cv2.imread('firstFrameGrayHog.png')
height,width,channel=img1.shape

arr = [[0]*height]*width


# Plotting pixel
for k in range(0,k):
    a = int(x[k])
    b = int(w[k])
    c = int(y[k])
    d = int(h[k])

    xa=int(a+3*b/6)
    xb=int(a+4*b/6)
    ya=int(c+7*d/8)
    yb=int(c+d)




    flag=0
    for i in range(xa,xb):
        for j in range(ya,yb):
            if i < width and j < height:
                if arr[i][j] <= 100:
                    flag=1
                elif arr[i][j]<=200:
                    flag=2
                elif arr[i][j]<=1040:
                    flag=3
                else:
                    flag=4
                arr[i][j]=arr[i][j]+1

    if flag==1:
        pxlValA,pxlValB,pxlValC=255,212,128
    elif flag==2:
        pxlValA,pxlValB,pxlValC=92,214,92
    elif flag==3:
        pxlValA,pxlValB,pxlValC=0,255,255
    elif flag==4:
        pxlValA,pxlValB,pxlValC=26,26,255




    for i in range(xa,xb):
        for j in range(ya,yb):
            if i<width and j<height:
                img1[j,i]=[pxlValA, pxlValB, pxlValC]


# Showing image
cv2.imshow('img',img1)
# Write onto original file
cv2.imwrite('firstFrameGray.png',img1)
#cv2.imwrite('firstFrameGrayHog.png',img1)
cv2.waitKey(0)
