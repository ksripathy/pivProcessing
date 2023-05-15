from PIL import Image, ImageDraw
import numpy as np

def imposePolygon(imWidth, imHeight, polygonVertices):

    dummyImage = Image.new('L', (imWidth,imHeight), 0)
    ImageDraw.Draw(dummyImage).polygon(polygonVertices, outline=1, fill=1)
    mask = np.array(dummyImage)[:,:] > 0
    
    return mask
