import copy
import numpy as np
import scipy as sp

def finite_differences(img_main):
  
  imagen_3d = copy.deepcopy(img_main)
  
  kernel_3d = np.array([[[0, 0, 0,],[0, -1, 1,],[0, 0, 0,]], [[0, 0, 0,],[0, -1, 0,],[0, 1, 0,]], [[0, 0, 0,],[0, -1, 0,],[0, 1, 0,]]])
  img_filt = sp.ndimage.convolve(imagen_3d, kernel_3d)
  
  return img_filt