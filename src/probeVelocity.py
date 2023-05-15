from scipy import interpolate
import numpy as np

def probeVelocity(windowsHorizontal, windowsVertical, velX, velY):
    
    velMag = np.sqrt(velX**2 + velY**2)    
    
    intpVelX = interpolate.RectBivariateSpline(windowsVertical, windowsHorizontal, velX)
    intpVelY = interpolate.RectBivariateSpline(windowsVertical, windowsHorizontal, velY)
    intpVelMag = interpolate.RectBivariateSpline(windowsVertical, windowsHorizontal, velMag)
    
    return intpVelX, intpVelY, intpVelMag
    
    