import math
import numpy as np
import cv2
img = cv2.imread("road.jpg", cv2.IMREAD_GRAYSCALE)
height = img.shape[0]
width = img.shape[1]
center = [height//2, width//2]
corners = cv2.goodFeaturesToTrack(img, 27, 0.01, 10)
corners = np.int0(corners)
corners = corners.astype(np.int)[:,0,:]
minx =corners[0][0]
maxx =corners[0][0]
miny =corners[0][1]
maxy =corners[0][1]
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
line = [maxx , (maxy + miny+miny)//2] if maxx < center[0] else [minx, ((maxy + miny+miny)//2)]
def tocm(pix):
    return round(pix/37.7952755906,2)
distance = math.sqrt((center[0]-line[0])**2+(center[1]-line[1])**2)
distance = tocm(distance)
print(''.center(74,'-'))
print('|',f"imageSize {tocm(height)} cm*{tocm(width)} cm".center(70),'|')
print('|',f'road in {tocm(maxx)} cm /n'.center(70),'|')
print('|',f'distance between line and center of img is {round(distance,2)} cm'.center(70),'|')
print(''.center(74,'-'))
