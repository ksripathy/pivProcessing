import numpy as np
from src.windowToDisp import windowToDisp

def pivInterrogation(im1Data, im2Data, imWidth, imHeight, windowSize, meanFilter=False, maskFilter=False):
    
    #Flip pixel data column-wise for plotting convenience
    
    im1DataFlip = np.flip(im1Data, axis = 0)
    im2DataFlip = np.flip(im2Data, axis = 0)
    
    #Divide image into interrogation windows
    numberOfColumns = int(imWidth/windowSize)
    numberOfRows = int(imHeight/windowSize)
    numberOfWindows = numberOfColumns * numberOfRows
    numberOfScannedPixels = numberOfWindows * windowSize**2
    
    #Numpy arrays for storing data in windows
    windowsHorizontalPx = np.arange(numberOfColumns + 1) * windowSize
    windowsVerticalPx = np.arange(numberOfRows + 1) * windowSize
    dispX = np.zeros((numberOfRows + 1,numberOfColumns + 1))
    dispY = np.zeros((numberOfRows + 1,numberOfColumns + 1))
    SNR = np.zeros((numberOfRows + 1,numberOfColumns + 1))
    
    #Interrogation scheme 
    for i in range(numberOfRows):
        for j in range(numberOfColumns):
            
            #Scanning all non-overlapping windows
            
            #Assigning pixel bounds for the window
            firstPixelX = j*windowSize
            lastPixelX = (j+1)*windowSize
            firstPixelY = i*windowSize
            lastPixelY = (i+1)*windowSize
            
            #Perform cross-correlation for non overlapping windows
            dispLocalX, dispLocalY, SNRLocal = windowToDisp(im2DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], im1DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], meanFilter)
            
            dispX[i,j] = dispLocalX
            dispY[i,j] = dispLocalY
            SNR[i,j] = SNRLocal
            
            #Scanning overlapping windows         
            if j+1 == numberOfColumns:
                firstPixelX = -windowSize
                lastPixelX = -1
                
                dispX[i,j+1], dispY[i,j+1], SNR[i,j+1] = windowToDisp(im2DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], im1DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], meanFilter)
                
            #Scanning last row
            if i+1 == numberOfRows:
                firstPixelY = -windowSize
                lastPixelY = -1
                
                dispX[i+1,j], dispY[i+1,j], SNR[i+1,j] = windowToDisp(im2DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], im1DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], meanFilter)
                
                if j+1 == numberOfColumns:
                    firstPixelX = -windowSize
                    lastPixelY = -1
                    
                    dispX[i+1,j+1], dispY[i+1,j+1], SNR[i+1,j+1] = windowToDisp(im2DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], im1DataFlip[firstPixelY:lastPixelY,firstPixelX:lastPixelX], meanFilter)
    
            
            
    #If the image has masking on then the region corresponding to mask
    #might have Nan values and needs to be filtered
            
    #Windows corresponding to NAN values in SNR
    if maskFilter:
        nanSNR = np.isnan(SNR)
        maskNan = nanSNR[:,:] == True
        
        dispX[maskNan] = 0
        dispY[maskNan] = 0
    
            
    return windowsHorizontalPx, windowsVerticalPx, dispX, dispY, SNR
    
    