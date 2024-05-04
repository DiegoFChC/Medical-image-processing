import nibabel as nib
import numpy as np
from App.auxFuntions.configuration_app import img_main, max_value, min_value, array_anotado


def normalizar_rango(matriz):
    """Normaliza una matriz 3D por rango."""
    minimo = np.min(matriz)
    maximo = np.max(matriz)
    return (matriz - minimo) / (maximo - minimo)


def upload_img_nii(url):
    global img_main, max_value, min_value, array_anotado
    img = nib.load(url)
    img = img.get_fdata()
    img_main = img
    max_value = np.max(img_main)
    min_value = np.min(img_main)
    # img_norm = normalizar_rango(img)
    size_img_x, size_img_y, size_img_z = img.shape
    array_anotado = np.zeros_like(img_main, dtype=np.int8)
    return (size_img_x, size_img_y, size_img_z, img_main)


def anotar_imagen(x, y, z, array):
    global array_anotado
    array_anotado[x, y, z] = array[x, y, z]


def reiniciar_anotacion():
    global img_main, array_anotado
    array_anotado = np.zeros_like(img_main, dtype=np.int8)
