import copy
import numpy as np


def k_means(it, puntos, img_main):
    img = copy.deepcopy(img_main)

    k = len(puntos)

    centroides = puntos

    new_img_k = np.zeros_like(img, dtype=np.int8)

    iteracion = 0
    while iteracion < it:
        print("iteracion:", iteracion)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(img.shape[2]):
                    if img[i, j, k] != 0:
                        diff = [abs(centroide - img[i, j, k])
                                for centroide in centroides]
                        new_img_k[i, j, k] = np.argmin(diff) + 1

        for i in range(len(centroides)):
            centroides[i] = np.mean(img[new_img_k == i+1])
        iteracion += 1

    # if k > 1:
    #     img_norm = normalizar_rango(new_img_k)

    print("Fin de k-means!!!")
    return new_img_k
