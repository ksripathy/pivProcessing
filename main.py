import os
import sys
from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt
    

#Configuring relative file locations
homeDir = os.path.dirname(__file__)
srcDir = os.path.join(homeDir,"src")
imDir = os.path.join(homeDir,"images")
plotDir = os.path.join(homeDir,"plots")

#Add src folder to python path
sys.path.append(srcDir)

from src.imageToDataPair import imageToDataPair
from src.windowToDisp import windowToDisp

im1Data, im2Data,imWidth, imHeight = imageToDataPair(imDir + "/Image_0001_a.tif", imDir + "/Image_0001_b.tif")

#Reproduce image

fig1, ax1 = plt.subplots()
ax1.imshow(np.transpose(im1Data), cmap='gray', vmin=0, vmax=255)

fig2, ax2 = plt.subplots()
ax2.imshow(np.transpose(im2Data))

windowSize = 64 #[px]

#Divide image into interrogotation windows
numberOfColumns = int(imWidth/windowSize) - 1
numberOfRows = int(imHeight/windowSize) - 1
numberOfWindows = numberOfColumns * numberOfRows
numberOfScannedPixels = numberOfWindows * windowSize**2

#Numpy arrays
windowsX = np.arange(numberOfColumns)
windowsY = np.arange(numberOfRows)
dispX = np.zeros((numberOfColumns,numberOfRows))
dispY = np.zeros((numberOfColumns,numberOfRows))
SNR = np.zeros((numberOfColumns,numberOfRows))

for j in range(numberOfRows):
    for i in range(numberOfColumns):
        
        firstPixelX = i*windowSize
        lastPixelX = (i+1)*windowSize
        firstPixelY = j*windowSize
        lastPixelY = (j+1)*windowSize
        
        dispLocalX, dispLocalY, SNRLocal = windowToDisp(im1Data[firstPixelX:lastPixelX,firstPixelY:lastPixelY], im2Data[firstPixelX:lastPixelX,firstPixelY:lastPixelY])
        
        dispX[i,j] = dispLocalX
        dispY[i,j] = dispLocalY
        SNR[i,j] = SNRLocal
        



'''im1DataLocal = im1Data[570:634,150:214]
im2DataLocal = im2Data[570:634,150:214]

dispX, dispY, corrSNR = windowToDisp(im1DataLocal,im2DataLocal)'''

'''im1DataFiltered = im1DataLocal - np.mean(im1DataLocal)
im2DataFiltered = im2DataLocal - np.mean(im2DataLocal)

normTerm = np.sqrt(np.sum(np.power(im1DataFiltered,2)) * np.sum(np.power(im2DataFiltered,2)))

crossCorrMap = sig.correlate(im1DataFiltered,im1DataFiltered)

top3 = np.argpartition(crossCorrMap, -3, axis=None)[-3:]
top3Read = np.unravel_index(top3, crossCorrMap.shape)

fig3,ax3 = plt.subplots()
ax3.imshow(crossCorrMap)'''



'''#Cross-correlation test
im1DataCorrIm2Data = sig.correlate(im1Data[:64,:64], im2Data[:64,:64])
im1DataCorrIm2Data2 = sig.correlate(im1Data[-64:,-64:], im2Data[-64:,-64:])
im1DataCorrIm2Data3 = sig.correlate(im1Data[688:752,:64], im2Data[688:752,:64])

im1DataReadStart = im1Data[:64,:64]
im2DataReadStart = im2Data[:64,:64]
im1DataReadEnd = im1Data[-64:,-64:]
im2DataReadEnd = im2Data[-64:,-64:]

#Top three entries in correlation matrix
top3 = np.argpartition(im1DataCorrIm2Data,-3,axis=None)[-3:]
top3Read = np.unravel_index(top3,im1DataCorrIm2Data.shape)

top32 = np.argpartition(im1DataCorrIm2Data2,-3,axis=None)[-3:]
top32Read = np.unravel_index(top32,im1DataCorrIm2Data2.shape)

top33 = np.argpartition(im1DataCorrIm2Data3,-3,axis=None)[-3:]
top33Read = np.unravel_index(top33,im1DataCorrIm2Data3.shape)

#Highest entry
top1 = im1DataCorrIm2Data.argmax()
top1TwoDim = np.unravel_index(im1DataCorrIm2Data.argmax(),im1DataCorrIm2Data.shape)''' 