import copy
import numpy as np

def median_filter(tamano_filtro, img_main):
    """
    Función que aplica un filtro de mediana a una imagen 3D (.nii).

    Argumentos:
      imagen_3d: La imagen 3D como un array de NumPy.
      tamano_filtro: El tamaño del filtro (un número impar positivo).

    Retorna:
      La imagen filtrada como un array de NumPy.
    """
    imagen_3d = copy.deepcopy(img_main)

    # Calcular el radio del filtro
    radio = (tamano_filtro - 1) // 2

    # Añadir bordes a la imagen para evitar errores de límites
    imagen_3d_pad = np.pad(
        imagen_3d, ((radio, radio), (radio, radio), (radio, radio)), mode='constant')

    # Inicializar la imagen filtrada
    imagen_filtrada = np.zeros_like(imagen_3d)

    # Recorrer cada voxel de la imagen original
    for i in range(imagen_3d.shape[0]):
        for j in range(imagen_3d.shape[1]):
            for k in range(imagen_3d.shape[2]):
                # Obtener los vecinos del voxel actual
                vecinos = imagen_3d_pad[i:i+tamano_filtro,
                                        j:j+tamano_filtro, k:k+tamano_filtro].flatten()

                # Calcular la mediana de los vecinos
                valor_mediana = np.median(vecinos)

                # Asignar la mediana al voxel filtrado correspondiente
                imagen_filtrada[i, j, k] = valor_mediana
    print("Fin de median-filter!!!")
    return imagen_filtrada