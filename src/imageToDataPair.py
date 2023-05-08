from PIL import Image
import numpy as np

def imageToDataPair(im1Location,im2Location):
    
    #Open images
    im1 = Image.open(im1Location)
    im2 = Image.open(im2Location)
    
    #Obtain Image sizes
    im1Width, im1Height = im1.size
    im2Width, im2Height = im2.size
    
    #Extract pixel data of images
    #Pillow scans image left to right and top to bottom
    im1Pix = im1.load()
    im2Pix = im2.load()
    
    #Translate pixel data into numpy data
    im1Data = np.zeros((im1Width,im1Height))
    im2Data = np.zeros((im2Width,im2Height))

    for i in range(im1Width):
        for j in range(im1Height):
            im1Data[i,j] = im1Pix[i,j]
            
    for i in range(im2Width):
        for j in range(im2Height):
            im2Data[i,j] = im2Pix[i,j]
            
    return im1Data, im2Data, im1Width, im1Height

    