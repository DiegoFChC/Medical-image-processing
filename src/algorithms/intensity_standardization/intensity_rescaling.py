import copy
import numpy as np

def intensity_rescaling(img_main):
    image = copy.deepcopy(img_main)
    min = np.min(image)
    max = np.max(image)
    new_image = (image - min)/(max - min)
    print("Fin de rescaling!!!")
    return new_image