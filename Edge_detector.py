import PIL
import PIL.Image
import math
import numpy 
import show_funcs
#Do arrays with Numpy instead of anything bro


def edge_getter(edge, max):
    """
    Helper function to assist with getting the outliers
            while applying a filter with mirrored edges.
    
    Parameters:
    - edge (int): The edge value to be adjusted
    - max (int): The maximum value for the edge

    Returns:
    - int: The adjusted edge value
    """

    if max < 1:
        raise ValueError("Max must be greater than 0")

    if edge < 0:
        edge = -edge
    elif edge >= max:
        edge = max-2-(edge-max)

    return edge


def gauss_blur(im, stddev):
    """
    Solution to Exercise 4.10
    Applies a filter to an image using gaussian blur

    Parameters:
    - im (PIL.Image.Image): The image to which the filter will be applied
    - stddev (float): The standard deviation of the gaussian filter

    Returns:
    - PIL.Image.Image: The image with the gaussian blur applied
    """

    if (5*stddev+1)%2 == 0:
        length = 5*stddev+2
    else:
        length = 5*stddev+1
    
    length = int(length//2)
    
    arr = []
    sum = 0
    for j in range(-length, length+1):
        arr.append(math.exp(-((j**2))/(2*(stddev**2))))
        sum += arr[j+length]

    s = 1/sum
    for i in range(len(arr)):
        arr[i] = arr[i]*s
    
    M = im.size[0]
    N = im.size[1]
    
    new_image = PIL.Image.new("L", (M, N))

    for i in range(M):
        for j in range(N):
            sum = 0
            for m in range(-length, length+1):
                edge = i+m
                while edge < 0 or edge >= M:
                    edge = edge_getter(edge, M)
                pix = im.getpixel((edge, j))        
                fil = arr[m+length]   
                sum += pix * fil
            new_image.putpixel((i, j), round(sum))
    
    for i in range(M):
        for j in range(N):
            sum = 0
            for n in range(-length, length+1):
                edge = j+n
                while edge < 0 or edge >= N:
                    edge = edge_getter(edge, N)
                pix = new_image.getpixel((i, edge))
                fil = arr[n+length]
                sum += pix * fil
            im.putpixel((i, j), round(sum))

    return im

#Check this stuff
def dimension_convolvex(im, filter):
    M = im.size[0]
    N = im.size[1]
    m = len(filter)//2

    new_image = PIL.Image.new("F", (M, N))

    for i in range(M):
        for j in range(N):
            sum = 0
            for m in range(-m, m+1):
                edge = i+m
                while edge < 0 or edge >= M:
                    edge = edge_getter(edge, M)
                pix = im.getpixel((edge, j))        
                fil = filter[m+1]   
                sum += pix * fil
            new_image.putpixel((i, j), sum)

    return new_image


#Edge cases require reflection
def dimension_convolvey(im, filter):
    M = im.size[0]
    N = im.size[1]
    m = len(filter)//2

    new_image = PIL.Image.new("F", (M, N))

    for i in range(M):
        for j in range(N):
            sum = 0
            for n in range(-m, m+1):
                edge = j+n
                while edge < 0 or edge >= N:
                    edge = edge_getter(edge, N)
                pix = im.getpixel((i, edge))        
                fil = filter[n+1]   
                sum += pix * fil
            new_image.putpixel((i, j), sum)

    return new_image

def get_orientation_sector(x, y):
    primes = numpy.dot([[math.cos(math.pi/8), -math.sin(math.pi/8)],[math.sin(math.pi/8), math.cos(math.pi/8)]], [x,y])
    if primes[1] < 0:
        primes[0] = -primes[0]
        primes[1] = -primes[1]
    if primes[0] >= 0:
        if primes[0] >= primes[1]:
            return 0
        else:
            return 1
    else: 
        if -primes[0] < primes[1]:
            return 2
        else: 
            return 3

def is_local_max(E_mag, pix, s_theta, t_lo):
    mc = E_mag[pix[0]][pix[1]]
    if mc < t_lo:
        return False
    else: 
        if s_theta == 0:
            ml = E_mag[pix[0]-1][pix[1]]
            mr = E_mag[pix[0]+1][pix[1]]
        elif s_theta ==1:
            ml = E_mag[pix[0]-1][pix[1]-1]
            mr = E_mag[pix[0]+1][pix[1]+1]
        elif s_theta ==2:
            ml = E_mag[pix[0]][pix[1]-1]
            mr = E_mag[pix[0]][pix[1]+1]
        elif s_theta ==3: 
            ml = E_mag[pix[0]-1][pix[1]+1]
            mr = E_mag[pix[0]+1][pix[1]-1]
    return (ml <= mc) and (mc >= mr)
        
def trace_threshold(E_nms, E_bin, pix, t_lo):
    M = len(E_nms)
    N = len(E_nms[0])
    E_bin.putpixel(pix, 1)
    u_l = max(pix[0]-1, 0)
    u_r = min(pix[0]+1, M-1)
    v_t = max(pix[1]-1, 0)
    v_b = min(pix[1]+1, N-1)
    for u in range(u_l, u_r):
        for v in range(v_t, v_b):
            pix = (u,v)
            if E_bin.getpixel(pix) == 0 and E_nms[u][v] >= t_lo:
                E_bin = trace_threshold(E_nms, E_bin, pix, t_lo)
    return E_bin


def color_edge_getter(im, stdv, t_lo):
    im_red, im_green, im_blue = im.split()

    red = gauss_blur(im_red, stdv)
    green = gauss_blur(im_green, stdv)
    blue = gauss_blur(im_blue, stdv)

    #These might be changed depending on how the tennis thing turns out
    grad_x = [-0.5, 0, 0.5]
    grad_y = [-0.5, 0, 0.5] #Strange T and the end of this, potentiallay should be [[-0.5], [0], [0.5]]

    M = red.size[0]
    N = red.size[1]

    red_x = dimension_convolvex(red, grad_x)
    green_x = dimension_convolvex(green, grad_x)
    blue_x = dimension_convolvex(blue, grad_x)
    
    red_y = dimension_convolvey(red, grad_y)
    green_y = dimension_convolvey(green, grad_y)
    blue_y = dimension_convolvey(blue, grad_y)

    E_mag = numpy.zeros((M, N))
    E_nms = numpy.zeros((M, N))
    E_x = numpy.zeros((M, N))
    E_y = numpy.zeros((M, N))
    E_bin = PIL.Image.new("1", (M, N))

    for i in range(M):
        for j in range(N):
            r_x = red_x.getpixel((i,j))
            g_x = green_x.getpixel((i,j))
            b_x = blue_x.getpixel((i,j))

            r_y = red_y.getpixel((i,j))
            g_y = green_y.getpixel((i,j))
            b_y = blue_y.getpixel((i,j))

            A = r_x**2 + g_x**2 + b_x**2
            B = r_y**2 + g_y**2 + b_y**2
            C = r_x*r_y + g_x*g_y + b_x*b_y

            D = math.sqrt((A-B)**2 + 4*(C**2))
            lamb = (A+B+D)/2
            E_mag[i][j] = math.sqrt(lamb)
            E_x[i][j] = A-B+D
            E_y[i][j] = 2*C

            E_bin.putpixel((i,j), 0)

    for u in range(1, M-2):
        for v in range(1, N-2):
            pixel = (u,v)
            s = get_orientation_sector(E_x[u][v], E_y[u][v])
            if is_local_max(E_mag, pixel, s, t_lo):
                E_nms[u][v] = E_mag[u][v]
    for u in range(1, M-2):
        for v in range(1, N-2):
            pixel = (u,v)
            if E_nms[u][v] >= t_lo and E_bin.getpixel(pixel) == 0: 
                E_bin = trace_threshold(E_nms, E_bin, pixel, t_lo)

    return E_bin
           
