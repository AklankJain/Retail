import numpy as np
import cv2
import matplotlib.pyplot as plt

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
img1 = cv2.imread('frameToCopyFrom.png')

trijal=cv2.imread('trijal.png')


#cv2.line(img1, (226, 64), (141, 288), (0, 0, 255), 2)
# img1 = cv2.imread('firstFrameGrayHog.png')
height, width, channel = img1.shape
print height, width


imgg=img1


for i in range(height):
    for j in range(width):
        imgg[i,j]=255



arr = [[0] * height] * width

for k in range(0, k):
    a = int(cx[k])
    b = int(cy[k])
    if a < width and b < height:
        if arr[a][b] <= 100:
            flag = 1
        elif arr[a][b] <= 600:
            flag = 2
        elif arr[a][b] <= 1000:
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
            #if checkPointSide(b, i):
            arr[i][b] = arr[i][b] + 1
            img1[b, i] = [pxlValA, pxlValB, pxlValC]

    for i in range(a - 2, a):
        if i>0:
            #if checkPointSide(b, i):
            arr[i][b] = arr[i][b] + 1
            img1[b, i] = [pxlValA, pxlValB, pxlValC]

    for i in range(b, b + 2):
        if i < height:
            #if checkPointSide(i, a):
            arr[a][i] = arr[a][i] + 1
            img1[i, a] = [pxlValA, pxlValB, pxlValC]

    for i in range(b - 2, b):
        if i >0:
            #if checkPointSide(i, a):
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


#crop_img = img1[80:288, 100:300] # Crop from x, y, w, h -> 100, 200, 300, 400 #cropping  for  street area
crop_img = img1[80:288, 100:300] # cropping for inside showroom
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
#cv2.imshow("cropped", crop_img)

resized_trijal = cv2.resize(trijal, (700, 700))
cv2.imshow('trijal',resized_trijal)
cv2.imwrite('Resized_trijal.png',resized_trijal)

cv2.imwrite('crop_img.png',crop_img)



img2=resized_trijal.copy()

for i in range(700):
    for j in range(700):
        img2[i,j]=(255,255,255)





#cv2.imshow('ssk', img2)

# Showing image


cv2.imshow('img', img1)

resized_img= cv2.resize(img1, (130, 130))
cv2.imshow('imgs', resized_img)

for i in range(270,400):
    for j in range(270,400):
        img2[i,j]=resized_img[i-270,j-270]

cv2.imshow('imgsh', img2)

print type(img2)
#print img2.shape
import pandas as pd

#df=pd.DataFrame(img2)
#print img2
np.savetxt('test.csv',img2.reshape(-1,img2.shape[-1]), delimiter=',',fmt='%.18e')

#np.savetxt("output.csv", img2, delimiter=",")  #Divay u need to edit it according to ur requirement.. Brp this is giving some error..
                                                #If you want this array just google it on how to do it.. search 2d aray to csv in python



alpha=0.5 #change it's value to maximize or minimize intensity

overlay = resized_trijal.copy()
output = resized_trijal.copy()

dest=img2.copy()

# apply the overlay
cv2.addWeighted(overlay, alpha,dest , 1 - alpha,0, output)

# show the output image
#print("alpha={}, beta={}".format(alpha, 1 - alpha))
cv2.imshow("Output", output)

cv2.imwrite('Output.png',output)

# Write onto original file
cv2.imwrite('firstFrameGray.png', img1)

# cv2.imwrite('firstFrameGrayHog.png',img1)
cv2.waitKey(0)
