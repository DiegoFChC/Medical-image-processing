import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import copy

size_img_x = 0
size_img_y = 0
size_img_z = 0
img_main = []
max_value = 1
min_value = 1
array_anotado = []

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


def thresholding(tau, deltaTau):
    global img_main
    img = copy.deepcopy(img_main)
    tau_init = tau
    t = 0
    tau_t = tau_init

    if tau != 0:
        img_th = img > tau_t
        print("Umbralizacion sencilla")
    else:
        print("isodata")
        while True:
            img_th = img > tau_t
            m_foreground = img[img_th == 1].mean()
            m_background = img[img_th == 0].mean()
            tau_new = 0.5 * (m_foreground + m_background)

            # print(tau_new - tau_t)
            if abs(tau_new - tau_t) < deltaTau:
                break
            else:
                tau_t = tau_new
    print("Fin de umbralización!!!")
    return img_th


def crecimiento_regiones_3d(tolerancia, punto_inicio, iteraciones):
    global img_main
    imagen = copy.deepcopy(img_main)

    # Valor a comparar con vecinos
    promedio_actual = imagen[punto_inicio]

    # Obtener las dimensiones de la imagen
    dim_x, dim_y, dim_z = imagen.shape

    # Crear una imagen binaria con todos los voxels como 0
    imagen_binaria = np.zeros_like(imagen, dtype=np.int8)

    # Cola para almacenar los nodos que se van a explorar
    cola = [punto_inicio]
    imagen_binaria[punto_inicio] = 1
    i = 0

    # Bucle principal
    while i < iteraciones and cola:
        # Extraer el primer elemento de la cola
        x, y, z = cola.pop(0)

        # Excluir los nodos no aceptados
        if (imagen_binaria[x, y, z] != 2):

            # Calcular promedio actual
            promedio_actual = np.mean(imagen[imagen_binaria == 1])

            # Bucle para definir vecinos y evaluar si se agregan a la region
            for dx, dy, dz in [(0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)]:
                # Si el vecino está dentro de la imagen
                if 0 <= x + dx < dim_x and 0 <= y + dy < dim_y and 0 <= z + dz < dim_z:
                    # Si el valor del vecino está dentro de la tolerancia y no ha sido analizado
                    if abs(promedio_actual - imagen[x + dx, y + dy, z + dz]) <= tolerancia and imagen_binaria[x + dx, y + dy, z + dz] != 2 and imagen_binaria[x + dx, y + dy, z + dz] != 1:
                        # Agregar el vecino a la cola
                        cola.append((x + dx, y + dy, z + dz))
                        imagen_binaria[x + dx, y + dy, z + dz] = 1
                    # Si no cumple con la tolerancia, se descarta (2 -> Marca para identificar si un boxel ha sido desechado)
                    else:
                        if imagen_binaria[x + dx, y + dy, z + dz] != 1:
                            imagen_binaria[x + dx, y + dy, z + dz] = 2

        i += 1

    # Los valores con 2 se pasan a 0
    imagen_binaria[imagen_binaria == 2] = 0
    print("Fin de crecimiento de regiones!!!")
    return imagen_binaria


def k_means(it, puntos):
    global img_main
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
                        diff = [abs(centroide - img[i, j, k]) for centroide in centroides]
                        new_img_k[i, j, k] = np.argmin(diff) + 1

        for i in range(len(centroides)):
            centroides[i] = np.mean(img[new_img_k == i+1])
        iteracion += 1
    
    # if k > 1:
    #     img_norm = normalizar_rango(new_img_k)
    
    print("Fin de k-means!!!")
    return new_img_k

def anotar_imagen(x, y, z, array):
    global array_anotado
    array_anotado[x, y, z] = array[x, y, z]

def reiniciar_anotacion():
    global img_main, array_anotado
    array_anotado = np.zeros_like(img_main, dtype=np.int8)