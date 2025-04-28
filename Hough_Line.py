#can maybe delete some of these later
import PIL
import PIL.Image
import math
import numpy 

#This is the place to look for bugs
def is_local_max(A, m, n, i, j): 
    for k in range(-1, 2):
        for l in range(-1, 2):
            if k == 0 and l == 0:
                continue

            i_real = i+k
            j_real = j+l

            if 0 <= i_real < m and 0 <= j_real < n:
                if A[i_real][j_real][0] > A[i][j][0]:
                    return False
    return True

def Ai_checker(Ai, x, y):

    if Ai[2] > y: 
        Ai[1] = x
        Ai[2] = y
    if Ai[4] < y: #Hi y
        Ai[3] = x
        Ai[4] = y
    return Ai

def hough_transform_lines(X, M, N, m, n, smin):
    # Input: X = (x0, . . .), a collection of 2D points; M, N, width and
    # height of the image plane; m, n, angular/radial accumulator steps;
    # smin, minimum line score (points on the line). Returns a sequence
    # L of detected lines.
    xr = (.5*M, .5*N)
    d_theta = math.pi/m
    dr = numpy.sqrt(M**2+N**2)/n 
    j0 = n//2

    A = numpy.zeros((m, n, 5))
    for k in range(len(X)):
        (x,y) = (X[k][0]-xr[0], X[k][1]-xr[1])
        for i in range(m):
            theta = d_theta*i
            r = x*math.cos(theta) + y*math.sin(theta) #This can be crazy performance improved (check book)
            j = j0 + round(r/dr)
            A[i][int(j)][0]+=1
            if A[i][int(j)][0] == 1:
                A[i][int(j)][1] = X[k][0]
                A[i][int(j)][2] = X[k][1] 
                A[i][int(j)][3] = X[k][0]
                A[i][int(j)][4] = X[k][1]
            else: 
                A[i][int(j)] = Ai_checker(A[i][int(j)], X[k][0], X[k][1])
                

    L = []
    for i in range(len(A)):
        for j in range(len(A[i])):
            if A[i][j][0] >= smin and is_local_max(A, m, n, i, j): 
                theta = d_theta*i
                r = (j-j0)*dr
                line = (theta, r, xr, A[i][j])
                L.append(line)

    return L
