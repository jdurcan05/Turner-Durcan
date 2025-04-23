import PIL
from PIL import Image
import math
import sys

from PIL import ImageDraw





def find_maxima(M, N, im):
    """
    Helper function in the Sobel class to find the hi and lo pix values of an image
        
    Parameters:
    - im (PIL.Image.Image): The image to be processed
    - M (int): The length of the image
    - N (int): The width of the image
        
    Returns: 
    - hilo (tuple) : A tuple with the min and max values of the image
    """
    hilo = [sys.maxsize, -sys.maxsize]
    for u in range(M):
        for v in range(N):
            pix = im.getpixel((u,v))
            if hilo[0] > pix:
                hilo[0] = pix
            if hilo[1] < pix:
                hilo[1] = pix
    return hilo

def make_i_x(E_x, M, N):
    """
    Helper function in the Sobel class to normalize the edge strength in the y direction

    Parameters: 
    - E_x (PIL.Image.Image): The image with the x-derivative applied
    - M (int): The length of the image
    - N (int): The width of the image

    Returns: 
    - i_x (PIL.Image.Image): A luminance image with the edge strength in the x direction
    """
    LUMINANCE_MAX = 255
    hilo = find_maxima(M, N, E_x)
    lo = hilo[0]
    hi = hilo[1]

    nex = Image.new("L", E_x.size)        
    for u in range(M):
        for v in range(N):
            nex.putpixel((u,v), round((E_x.getpixel((u,v))-lo)/(hi-lo)*LUMINANCE_MAX))
        
    return nex

def make_i_y (E_y, M, N):
    """
    Helper function in the Sobel class to normalize the edge strength in the y direction

    Parameters: 
    - E_y (PIL.Image.Image): The image with edge strength in the y direction
    - M (int): The length of the image
    - N (int): The width of the image

    Returns: 
    - i_y (PIL.Image.Image): A luminance image with the edge strength in the y direction
    """
    hilo = find_maxima(M, N, E_y)
    lo = hilo[0]
    hi = hilo[1]
    LUMINANCE_MAX = 255
    ney = Image.new("L", E_y.size)        
    for u in range(M):
        for v in range(N):
            ney.putpixel((u,v), round((E_y.getpixel((u,v))-lo)/(hi-lo)*LUMINANCE_MAX))
    return ney  
