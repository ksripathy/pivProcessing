#For when both the image pair is in one image

from PIL import Image, ImageDraw
import numpy as np
from src.imposePolygon import imposePolygon


def imageToDataPairV3(imPath, opticalMask = False):
    
    #Open image
    im = Image.open(imPath)
    
    #Translate image to numpy array
    imData = np.array(im)
    
    #Obtain image dimensions
    imWidth, imHeight = im.size
    
    #Split image
    im1Data = imData[:int(0.5*imHeight), :]
    im2Data = imData[int(0.5*imHeight):, :]
    
    #Impose optical mask shaped like a polygon
    if opticalMask:
        polygonVertices = [(191,627), (529,751), (657, 433), (311, 302)]
        mask = imposePolygon(imWidth, imHeight, polygonVertices)
        im1Data[mask] = 0
        im2Data[mask] = 0
    
    return im1Data, im2Data, imWidth, int(imHeight*0.5)
    