import copy
import numpy as np

def z_score(background_intensity, img_main):
    # mean_value = image.mean()
    # std_value = image.std()
    image = copy.deepcopy(img_main)
    mean_value = image[image > background_intensity].mean()
    std_value = image[image > background_intensity].std()
    img_zscore = (image - mean_value) / std_value
    print("Fin de z-score!!!")
    return img_zscore