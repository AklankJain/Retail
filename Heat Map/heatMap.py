
#To be used for entrance

import numpy as np
import cv2

m = (288 - 64) / (144 - 226)


def checkPointSide(xA, yA):
    # if xA!=226 and (yA-64)/(xA-226)-((288-64)/(141-226))<=0:
    if (288 - xA) - m * (141 - yA) <= 0:
        return 1
    else:
        return 0


data = np.loadtxt('co-ordinates.csv', delimiter=',')
# data = np.loadtxt('datapoints.csv', delimiter=',')

# Putting data from csv file to variables
x = data[:, 0]
y = data[:, 1]
w = data[:, 2]
h = data[:, 3]

cx = data[:, 4]
cy = data[:, 5]

# Taking out size of the file
k = x.shape[0]

# Converting npArray to simple array
np.asarray(x)
np.asarray(y)
np.asarray(w)
np.asarray(h)

np.asarray(cx)
np.asarray(cy)

# Reading image
img1 = cv2.imread('firstFrameGray.png')

cv2.line(img1, (226, 64), (141, 288), (0, 0, 255), 2)
# img1 = cv2.imread('firstFrameGrayHog.png')
height, width, channel = img1.shape
print height, width


arr = [[0] * height] * width

for k in range(0, k):
    a = int(cx[k])
    b = int(cy[k])
    if a < width and b < height:
        if arr[a][b] <= 10:
            flag = 1
        elif arr[a][b] <= 30:
            flag = 2
        elif arr[a][b] <= 50:
            flag = 3
        else:
            flag = 4


    if flag == 1:
        pxlValA, pxlValB, pxlValC = 255, 212, 128
    elif flag == 2:
        pxlValA, pxlValB, pxlValC = 92, 214, 92
    elif flag == 3:
        pxlValA, pxlValB, pxlValC = 0, 255, 255
    elif flag == 4:
        pxlValA, pxlValB, pxlValC = 26, 26, 255

    for i in range(a, a + 2):
        if i < width:
            if checkPointSide(b, i):
                arr[i][b] = arr[i][b] + 1
                img1[b, i] = [pxlValA, pxlValB, pxlValC]

    for i in range(a - 2, a):
        if i>0:
            if checkPointSide(b, i):
                arr[i][b] = arr[i][b] + 1
                img1[b, i] = [pxlValA, pxlValB, pxlValC]

    for i in range(b, b + 2):
        if i < height:
            if checkPointSide(i, a):
                arr[a][i] = arr[a][i] + 1
                img1[i, a] = [pxlValA, pxlValB, pxlValC]

    for i in range(b - 2, b):
        if i >0:
            if checkPointSide(i, a):
                arr[a][i] = arr[a][i] + 1
                img1[i, a] = [pxlValA, pxlValB, pxlValC]

"""
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



"""

# Showing image
cv2.imshow('img', img1)
# Write onto original file
cv2.imwrite('firstFrameGray.png', img1)

# cv2.imwrite('firstFrameGrayHog.png',img1)
cv2.waitKey(0)