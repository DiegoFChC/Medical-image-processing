import nibabel as nib
import numpy as np
import customtkinter as ctk
import tkinter as tk

class Algorithm_Status:
    def __init__(self):
        self.img_main = []
        self.annotated_array = []
        self.size_img_x = 0
        self.size_img_y = 0
        self.size_img_z = 0
        self.max_value = 1
        self.min_value = 1

    # Getters (accessor methods)
    def get_img_main(self):
        return self.img_main

    def get_annotated_array(self):
        return self.annotated_array

    def get_size_img_x(self):
        return self.size_img_x

    def get_size_img_y(self):
        return self.size_img_y

    def get_size_img_z(self):
        return self.size_img_z

    def get_max_value(self):
        return self.max_value

    def get_min_value(self):
        return self.min_value

    # Setters (mutator methods)
    def set_img_main(self, new_image):
        self.img_main = new_image
        
    # def set_annotated_array(self, new_annotated_array):
    #     self.annotated_array = new_annotated_array

    def set_annotated_array(self, x, y, z, array):
        self.annotated_array[x, y, z] = array[x, y, z]
        
    def reset_annotated_array(self):
        self.annotated_array = np.zeros_like(self.img_main, dtype=np.int8)

    def set_size_img_x(self, new_size_x):
        self.size_img_x = new_size_x

    def set_size_img_y(self, new_size_y):
        self.size_img_y = new_size_y

    def set_size_img_z(self, new_size_z):
        self.size_img_z = new_size_z

    def set_max_value(self, new_max_value):
        self.max_value = new_max_value

    def set_min_value(self, new_min_value):
        self.min_value = new_min_value

    def upload_img_nii(self, url):
        img = nib.load(url)
        img = img.get_fdata()
        self.img_main = img
        self.max_value = np.max(self.img_main)
        self.min_value = np.min(self.img_main)
        self.size_img_x, self.size_img_y, self.size_img_z = img.shape
        self.annotated_array = np.zeros_like(self.img_main, dtype=np.int8)
        return (self.size_img_x, self.size_img_y, self.size_img_z, self.img_main)
    
    def normalize_range(matriz):
        """Normaliza una matriz 3D por rango."""
        minimo = np.min(matriz)
        maximo = np.max(matriz)
        return (matriz - minimo) / (maximo - minimo)
    
    def export_annotations(self, name):
        img_uint8 = self.annotated_array.astype(np.float32)
        nii_img = nib.Nifti1Image(img_uint8, affine=np.eye(4))
        nib.save(nii_img, f"src/saved_processes/anotation_{name}.nii")
    