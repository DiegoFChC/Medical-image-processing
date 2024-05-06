import copy
import numpy as np


def region_growing(tolerancia, punto_inicio, iteraciones, img_main):
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
