from scipy import signal as sig
import numpy as np

#Function to obtain displacement in pixels from a pair of interrogoation windows
def windowToDisp(im1DataLocal,im2DataLocal, meanFilter=False):
    
   windowHeight, windowWidth = np.shape(im1DataLocal) 
   
   #Subtract mean value from window
   if meanFilter:
       im1DataFiltered = im1DataLocal - np.mean(im1DataLocal)
       im2DataFiltered = im2DataLocal - np.mean(im2DataLocal)
       
   else:
       im1DataFiltered = im1DataLocal
       im2DataFiltered = im2DataLocal
   
   #Normalization factor
   normTerm = np.sqrt(np.sum(np.power(im1DataFiltered,2)) * np.sum(np.power(im2DataFiltered,2)))
   
   #Obtain normalized cross-correlation map of the window pairs
   crossCorrMap = sig.correlate(im1DataFiltered,im2DataFiltered)/normTerm
   
   #Obtain two highest values in the correlation map. The indices are for a flattened array
   #With argpartition an array is created such that values before and after the indicated index
   #will le lesser and greater than the value at the selected index respectively 
   top2IndicesFlat = np.argpartition(crossCorrMap, -2, axis=None)[-2:]
   
   #Decode the above indices in the original 2D array. Output is in the form of a tuple
   #of indices of different dimensions
   top2Indices = np.unravel_index(top2IndicesFlat,crossCorrMap.shape)
   
   #Obtain displacement and SNR
   
   #Values corresponding to top two indices
   crossCorrMapT1 = crossCorrMap[top2Indices[0][0]][top2Indices[1][0]]
   crossCorrMapT2 = crossCorrMap[top2Indices[0][1]][top2Indices[1][1]]
   
   if crossCorrMapT1 >= crossCorrMapT2:
       #For zero displacement, max cross-corr will occur at the index of 
       #(windowWidth-1,windowHeight-1). Thus non-zero displacements will 
       #be computed with respect to this reference
       avgWindowDispY = top2Indices[0][0] - (windowHeight - 1) 
       avgWindowDispX = top2Indices[1][0] - (windowWidth - 1)
       crossCorrSNR = crossCorrMapT1/crossCorrMapT2
       
   else:
       avgWindowDispY = top2Indices[0][1] - (windowHeight - 1)
       avgWindowDispX = top2Indices[1][1] - (windowWidth - 1)
       crossCorrSNR = crossCorrMapT2/crossCorrMapT1

   return avgWindowDispX, avgWindowDispY, crossCorrSNR
   
   
    
    
    
