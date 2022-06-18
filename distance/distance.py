# import module neaded
import math
import numpy as np
import cv2
# fuction that convert pix to cm
def tocm(pix):
    return round(pix/37.7952755906,2)
# import image with opencv module
img = cv2.imread("road.jpg", cv2.IMREAD_GRAYSCALE)
# compute height and width and center of image
height = img.shape[0]
width = img.shape[1]
center = [height//2, width//2]
# detect edge of the line in pixle
corners = cv2.goodFeaturesToTrack(img, 27, 0.01, 10)
# casted to int
corners = np.int0(corners)
# get spesial array that neaded
corners = corners.astype(np.int)[:,0,:]
#compute min[x,y] and max[x,y] of the line
minx =corners[0][0]
maxx =corners[0][0]
miny =corners[0][1]
maxy =corners[0][1]
# if line have greater than 4 edge (top botton left right)
if len(corners) >=4:
    for i in corners:
        if i[0] > maxx:
            maxx = i[0]
        if i[0] < minx:
            minx = i[0]
        if i[1] > maxy:
            maxy = i[1]
        if i[1] < miny:
            miny = i[1]
# define an array that determine wich edge can use for compute distance
line = [maxx , (maxy + miny+miny)//2] if maxx < center[0] else [minx, ((maxy + miny+miny)//2)]
# compute distance
distance = math.sqrt((center[0]-line[0])**2+(center[1]-line[1])**2)
# show result
print(''.center(74,'-'))
print('|',f"imageSize {tocm(height)} cm * {tocm(width)} cm".center(70),'|')
print('|',f" {height} px * {width} px".center(70),'|')
print('|','------------------------------'.center(70),'|')
print('|',f'road in {tocm(maxx)} cm '.center(70),'|')
print('|',f' {maxx} px '.center(70),'|')
print('|','------------------------------'.center(70),'|')
print('|',f'distance between line and center of img is {round(tocm(distance),2)} cm'.center(70),'|')
print('|',f' {round(distance,2)} px'.center(70),'|')
print(''.center(74,'-'))
