from PIL import Image, ImageDraw
import numpy as np
from src.imposePolygon import imposePolygon


def imageToDataPairV2(im1Location, im2Location, opticalMask = False):
    
    #Open images
    im1 = Image.open(im1Location)
    im2 = Image.open(im2Location)
    
    #Translate image to numpy array
    im1Data = np.array(im1)
    im2Data = np.array(im2)
    
    #Obtain image dimensions
    imWidth, imHeight = im1.size
    
    #Impose optical mask shaped like a polygon
    if opticalMask:
        polygonVertices = [(191,627), (529,751), (657, 433), (311, 302)]
        mask = imposePolygon(imWidth, imHeight, polygonVertices)
        im1Data[mask] = 0
        im2Data[mask] = 0
    
    return im1Data, im2Data, imWidth, imHeight