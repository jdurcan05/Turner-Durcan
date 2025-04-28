import Edge_detector
import Hough_Line
import PIL
import PIL.Image
import Hough_Line
import numpy 
import math
from PIL import ImageDraw

def point_slope_extension(x1, y1, x2, y2):
    xer = x2-x1
    if xer == 0:
        slope = 0
    else:
        slope = (y2-y1) / (x2-x1)
    x2 = x1 + ((10000-y1) /slope) 
    
    return (x2, 10000, slope)

def get_line_endpoints(line):
    x1 = line[3][1]
    y1 = line[3][2]
    x2 = line[3][3]
    y2 = line[3][4]
    (x2, y2, slope) = point_slope_extension(x1, y1, x2, y2)
    return [(x1, y1), (x2, y2), slope]


im = PIL.Image.open("still.jpg")
im = Edge_detector.color_edge_getter(im, .4, 30)

X = []
arr = numpy.asarray(im)
for y in range(arr.shape[0]):
    for x in range(arr.shape[1]):
        if arr[y][x] > 0:
            X.append((x, y))

L = Hough_Line.hough_transform_lines(X, im.size[0], im.size[1], 180, 100, 600)
im2 = PIL.Image.new("1", im.size)
A = numpy.zeros(len(L))
for i in range(len(L)):
    # print(L[i][0], L[i][3][0])
    A[i] = L[i][3][0]
A.sort()

for line in L:
    # if line[3][0] >= A[-4]:
    #     # endpoints = get_line_endpoints(line)
    # if line[0] > 2:
    endpoints = get_line_endpoints(line) 
    for (x1, y1), (x2, y2), slope in [endpoints]:
        if abs(slope) > 1:
            PIL.ImageDraw.Draw(im2).line((x1, y1, x2, y2), fill=255, width=1)

    
im2.show()