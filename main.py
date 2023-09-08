import os
import sys
from scipy import signal as sig
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.axes_grid1 import make_axes_locatable
#%matplotlib widget

from PIL import Image, ImageDraw
    

#Configuring relative file locations
homeDir = os.path.dirname(__file__)
srcDir = os.path.join(homeDir,"src")
imDir = os.path.join(homeDir,"images")
plotDir = os.path.join(homeDir,"plots")

#Add src folder to python path
sys.path.append(srcDir)

#from src.imageToDataPairV2 import imageToDataPairV2
from src.imageToDataPairV3 import imageToDataPairV3
from src.pivInterrogation import pivInterrogation
from src.probeVelocity import probeVelocity
from src.imposePolygon import imposePolygon

#Input parameters
windowSize = 32
meanFilter = True #SUbtract mean value from windows
opticalMask = False #Replace pixel values with zero for locations at object. Warning: Optical mask is not implemented for lab exercise
maskFilter = True #Replace flowfield values with zero for regions with NaN SNR
deltaT = 70e-6 #[m]
pixelSize = 4.40e-6 #[m]
observedFoV = 192.38 * 1e-3 #From calibration image with mm paper

im1Data, im2Data, imWidth, imHeight = imageToDataPairV3(imDir + "/labExer/B00001.tif", opticalMask)

opticMagnification = imWidth * pixelSize / observedFoV

#Reproduce image

pixelsX, pixelsY= np.meshgrid(np.arange(imWidth), np.arange(imHeight))

fig4, ax4 = plt.subplots()
ax4.contourf(pixelsX, pixelsY, np.flip(im1Data*1000, axis=0))

fig5, ax5 = plt.subplots()
ax5.contourf(pixelsX, pixelsY, np.flip(im2Data*1000, axis=0))

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
velMag = np.sqrt(velX**2 + velY**2)

#Plotting results

xArg, yArg = np.meshgrid(windowsHorizontalMillimetres,windowsVerticalMillimetres)

polygonVertices = np.array([[194,409],[521,291],[640,610],[314,731]])*(pixelSize/opticMagnification)*1e3

fig6, ax6 = plt.subplots()
#ax6.contourf(xArg, yArg, SNR)
velCntr = ax6.contourf(xArg, yArg, velMag, levels=np.linspace(0,15,300), cmap = plt.colormaps["rainbow"])
#ax6.add_patch(Polygon(polygonVertices))
ax6.quiver(xArg, yArg, velX, velY)
ax6.set_xlabel("x [mm]")
ax6.set_ylabel("y [mm]")
ax6.set_title(f"Velocity contour [$ms^{{-1}}$]")
#fig6.colorbar(velCntr, ax=ax6, orientation="horizontal", fraction = 0.046, pad=0.04)
#fig6.tight_layout()

# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax6)
cax = divider.append_axes("right", size="5%", pad=0.05)
   
fig6.colorbar(velCntr, cax=cax)

fig6.savefig(plotDir + "/pivCodeVelcField.png", dpi=600)

fig7, ax7 = plt.subplots()
snrCntr = ax7.contourf(xArg, yArg, SNR, levels=48, cmap = plt.colormaps["rainbow"])
#ax7.add_patch(Polygon(polygonVertices))
#ax7.quiver(xArg, yArg, velX, velY)
ax7.set_xlabel("x [mm]")
ax7.set_ylabel("y [mm]")
ax7.set_title(f"Cross-correlation SNR [-]")
#fig6.colorbar(velCntr, ax=ax6, orientation="horizontal", fraction = 0.046, pad=0.04)
#fig6.tight_layout()

# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider2 = make_axes_locatable(ax7)
cax2 = divider2.append_axes("right", size="5%", pad=0.05)
   
fig7.colorbar(snrCntr, cax=cax2)

fig7.savefig(plotDir + "/pivCodeSNR.png", dpi=600)

intpVelX, intpVelY, intpVelMag = probeVelocity(windowsHorizontalMillimetres, windowsVerticalMillimetres, velX, velY)

velFreestream = intpVelMag(1000,100)
print("Freestream velocity:",velFreestream)

velMaxRev = np.min(velX)
print("Max reverse velocity:", velMaxRev)