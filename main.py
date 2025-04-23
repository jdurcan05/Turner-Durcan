import Edge_detector
import Hough_Line
import PIL
import PIL.Image
import Hough_Line
import numpy 
import math
from PIL import ImageDraw

def get_line_endpoints(line):
    theta = line[0]
    r = line[1]
    xr = line[2]  
    co = math.cos(theta)
    si = math.sin(theta)
    x = co*r + xr[0]
    y = si*r + xr[1]

    x1 = int(x + 1000*(-si))
    y1 = int(y + 1000*(co))
    x2 = int(x - 1000*(-si))
    y2 = int(y - 1000*(co))
    
    return [(x1, y1), (x2, y2)]


im = PIL.Image.open("image_on_line_free.jpg")
im = Edge_detector.color_edge_getter(im, 1, 20)

X = []
arr = numpy.asarray(im)
for y in range(arr.shape[0]):
    for x in range(arr.shape[1]):
        if arr[y][x] > 0:
            X.append((x, y))

L = Hough_Line.hough_transform_lines(X, im.size[0], im.size[1], 180, 100, 50)
im2 = PIL.Image.new("1", im.size)

A = numpy.zeros(len(L))
for i in range(len(L)):
    A[i] = L[i][3]
A.sort()

for line in L:
    if line[3] >= A[-4]:
        endpoints = get_line_endpoints(line)
    
        for (x1, y1), (x2, y2) in [endpoints]:
            PIL.ImageDraw.Draw(im2).line((x1, y1, x2, y2), fill=255, width=1)

    
im2.show()