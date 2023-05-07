import os
import sys

#Configuring relative file locations
homeDir = os.path.dirname(__file__)
srcDir = os.path.join(homeDir,"src")
imDir = os.path.join(homeDir,"images")
plotDir = os.path.join(homeDir,"plots")

#Add src folder to python path
sys.path.append(srcDir)

from imageToDataPair import imageToDataPair
im1Data, im2Data = imageToDataPair(imDir + "/Image_0001_a.tif", imDir + "/Image_0001_b.tif")