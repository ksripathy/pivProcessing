import os
import sys
from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

from PIL import Image, ImageDraw
    

#Configuring relative file locations
homeDir = os.path.dirname(__file__)
srcDir = os.path.join(homeDir,"src")
imDir = os.path.join(homeDir,"images")
plotDir = os.path.join(homeDir,"plots")

#Add src folder to python path
sys.path.append(srcDir)

from src.imageToDataPairV2 import imageToDataPairV2
from src.pivInterrogation import pivInterrogation
from src.probeVelocity import probeVelocity
from src.imposePolygon import imposePolygon

#Input parameters
windowSize = 64
meanFilter = True #SUbtract mean value from windows
opticalMask = True #Replace pixel values with zero for locations at object
maskFilter = True #Replace flowfield values with zero for regions with NaN SNR
deltaT = 80e-6 #[m]
pixelSize = 6.45e-6 #[m]
opticMagnification = 0.1

im1Data, im2Data, imWidth, imHeight = imageToDataPairV2(imDir + "/Image_0001_a.tif", imDir + "/Image_0001_b.tif", opticalMask)

#Reproduce image

pixelsX, pixelsY= np.meshgrid(np.arange(imWidth), np.arange(imHeight))

fig4, ax4 = plt.subplots()
ax4.contourf(pixelsX, pixelsY, np.flip(im1Data, axis=0))

windowsHorizontalPx, windowsVerticalPx, dispPxX, dispPxY, SNR = pivInterrogation(im1Data, im2Data, imWidth, imHeight, windowSize, meanFilter, maskFilter)

#FOV in mm
windowsHorizontalMillimetres = windowsHorizontalPx * (pixelSize/opticMagnification)*1e3
windowsVerticalMillimetres = windowsVerticalPx * (pixelSize/opticMagnification)*1e3

#Displacements in object plane
dispX = (dispPxX * pixelSize)/opticMagnification
dispY = (dispPxY * pixelSize)/opticMagnification

#Velocities in object plane
velX = dispX/deltaT
velY = dispY/deltaT


xArg, yArg = np.meshgrid(windowsHorizontalMillimetres,windowsVerticalMillimetres)

polygonVertices = np.array([[194,409],[521,291],[640,610],[314,731]])*(pixelSize/opticMagnification)*1e3

fig6, ax6 = plt.subplots()
ax6.contourf(xArg, yArg, SNR)
ax6.add_patch(Polygon(polygonVertices))
ax6.quiver(xArg, yArg, velX, velY)

intpVelX, intpVelY, intpVelMag = probeVelocity(windowsHorizontalMillimetres, windowsVerticalMillimetres, velX, velY)

velFreestream = intpVelMag(0,0)
print("Freestream velocity:",velFreestream)

velMaxRev = np.min(velX)
print("Max reverse velocity:", velMaxRev)