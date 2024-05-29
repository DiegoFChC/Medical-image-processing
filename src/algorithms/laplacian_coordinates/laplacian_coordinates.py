import numpy as np
from scipy import ndimage
from scipy.sparse import lil_matrix, find, diags, csr_matrix
import scipy.sparse.linalg as spla
# from skimage.measure import block_reduce
# import math

# Matriz de adyacencia con pesos - Ecuacion 1
def ecuacion1(imagen, beta = 1):
  vecindad = [(0, 1), (0, -1), (1, 0), (-1, 0)]
  # Crear una matriz de adyacencia vacía
  boxeles = imagen.shape[0] * imagen.shape[1]
  # print('cantidad de boxeles:', boxeles)
  matriz_adyacencia = lil_matrix((boxeles, boxeles))

  # Para calcular el indice lineal
  nx, ny = imagen.shape

  # voxeles visitados
  # visitados = np.zeros((boxeles, boxeles))

  # Para sigma
  # diferencias = np.zeros((boxeles, boxeles))

  # Para calcular el peso
  # sigma = np.max(diferencias)
  # print(sigma)

  def calcular_peso(I_i, I_j, beta, sigma):
    # print(beta, sigma)
    # peso = (-1) * ((beta*(np.abs(I_i - I_j) ** 2))/sigma)
    peso = (-1) * ((beta*(np.abs(I_i - I_j) ** 2)) / sigma)
    # print(peso)
    return np.exp(peso)

  # Calculo de las diferencias entre intensidades de vecinos para hallar la máxima
  diff_array = []

  # Recorrer cada pixel en el arreglo 2D
  for i in range(imagen.shape[0]):
    for j in range(imagen.shape[1]):
      # Obtener el valor del pixel actual
      current_pixel = imagen[i, j]

      # Calcular las diferencias con los vecinos
      # Arriba
      if i > 0:
        diff_array.append(np.abs(current_pixel - imagen[i - 1, j]))

      # Abajo
      if i < imagen.shape[0] - 1:
        diff_array.append(np.abs(current_pixel - imagen[i + 1, j]))

      # Izquierda
      if j > 0:
        diff_array.append(np.abs(current_pixel - imagen[i, j - 1]))

      # Derecha
      if j < imagen.shape[1] - 1:
        diff_array.append(np.abs(current_pixel - imagen[i, j + 1]))

  sigma = np.max(diff_array)
  # print("dif", np.max(diff_array), np.min(diff_array))
  # print('len', len(diff_array))
  # print('len2', imagen.shape[0]*imagen.shape[1])
  # sigma = 1

  # Recorrer cada elemento del array 3D
  for i in range(imagen.shape[0]):
      for j in range(imagen.shape[1]):
              # Calcular el índice lineal del nodo actual
              nodo = i * ny + j

              # Conectar el nodo con sus vecinos
              for di, dj in vecindad:
                  ni, nj = i + di, j + dj

                  # Verificar que el vecino esté dentro del array y que no haya sido visitado antes
                  if 0 <= ni < imagen.shape[0] and 0 <= nj < imagen.shape[1]:
                      # Calcular el índice lineal del vecino
                      vecino = ni * ny + nj

                      # if visitados[nodo, vecino] != 1 or visitados[vecino, nodo] != 1 or True:
                      if True:

                        # Para control
                        # visitados[nodo, vecino] = 1
                        # visitados[vecino, nodo] = 1
                        # diferencias[nodo, vecino] = np.abs(imagen[i, j] - imagen[ni, nj])

                        # sigma = np.max(diferencias) + np.power(10.0, -6)
                        # sigma = np.max(np.abs(imagen[i, j] - imagen[ni, nj])) + np.power(10.0, -6)

                        # Calcular el peso de la arista
                        # peso = abs(imagen[i, j] - imagen[ni, nj])
                        peso = calcular_peso(imagen[i, j], imagen[ni, nj], beta, sigma)
                        # print("peso:", peso, imagen[i, j], imagen[ni, nj], beta, sigma)
                        if peso == 0:
                            peso = np.power(10.0, -6)

                        # print(nodo, vecino)

                        # Añadir la arista a la matriz de adyacencia
                        matriz_adyacencia[nodo, vecino] = peso

  # Convertir la matriz de adyacencia a formato CSR para un procesamiento más eficiente
  matriz_adyacencia = matriz_adyacencia.tocsr()
  return matriz_adyacencia
  # print("peso:", peso(1,5, beta, sigma))
  # print(visitados)
  # print(diferencias)
  # print(np.max(diferencias))

# matriz_adyacencia = ecuacion1(imagen_proyecto)
# print(matriz_adyacencia)


# Suma de los pesos asociados a un boxel
def array_di(matriz_adyacencia, shape_img):
    # Crear un array 3D lleno de ceros con la misma forma que el array original
    array2d = np.zeros(shape_img)

    # Obtener las filas, columnas y valores de la matriz de adyacencia
    filas, columnas, valores = find(matriz_adyacencia)

    # Recorrer cada arista en la matriz de adyacencia
    for fila, valor in zip(filas, valores):
        # Calcular las coordenadas 2D del nodo
        i = fila // shape_img[1]
        j = fila % shape_img[1]

        # Sumar el peso de la arista al pixel correspondiente en el array 2D
        array2d[i, j] += valor

    return array2d

# pesos_di = array_di(matriz_adyacencia, imagen_proyecto.shape)
# print(pesos_di)


# Resolviendo el sistema de ecuaciones - Ecuacion 7
def solve_linear_system(di, m_adyacencia, imagen, semillas_background, semillas_foreground):
  # (Is + L2)x = b

  #######################################
  #                   L
  #######################################
  # Aplanamos di
  di_flatten = di.flatten()

  # L = D - W    -> Dii = di, W = Pesos (Matriz de adyacencia)
  L = diags(di_flatten) - m_adyacencia

  # Evitamos valores de 0
  L += np.power(10.0, -6) * diags(np.ones(len(di_flatten)))

  #######################################
  #                   Is
  #######################################
  '''
  Matriz diagonal que tiene todas las semillas.
  '''
  Is = np.zeros_like(imagen)
  b = np.zeros_like(imagen)

  for semilla in semillas_background:
      # print(semilla)
      Is[(semilla)] = 1
      b[(semilla)] = imagen[(semilla)]
  for semilla in semillas_foreground:
      # print(semilla)
      Is[(semilla)] = 1
      b[(semilla)] = imagen[(semilla)]

  b_flatten = b.flatten()
  Is_flatten = Is.flatten()

  Is_diagonal = diags(Is_flatten)

  minimizar = Is_diagonal + (L ** 2)


  ## Hallamos x
  minimizar_sparse = csr_matrix(minimizar)
  x = spla.cg(minimizar_sparse, b_flatten)

  return x[0]


# x_result = solve_linear_system(pesos_di, matriz_adyacencia, imagen_proyecto, array_background, array_foreground)
# print(x_result)

# Etiquetado final
def etiquetado_final(imagen, soluciones, semillas_background, semillas_foreground):
  new_image = np.zeros_like(imagen)

  # Ecuacion 3
  # Promedio de intensidades de background y foreground
  # valores_background = np.mean(imagen[semillas_background[:, 0], semillas_background[:, 1]])
  # valores_foreground = np.mean(imagen[semillas_foreground[:, 0], semillas_foreground[:, 1]])

  # promedio = (np.sum(valores_background) + np.sum(valores_foreground)) / 2
  
  valores_background = np.mean(imagen[semillas_background])
  valores_foreground = np.mean(imagen[semillas_foreground])

  promedio = ((valores_background) + (valores_foreground)) / 2
  print(promedio, valores_background, valores_foreground)
  for i, xi in enumerate(soluciones):

    coordenada = np.unravel_index(i, imagen.shape)

    if xi < promedio:
       new_image[coordenada] = 1
      #  new_image[coordenada] = imagen[coordenada]

  return new_image


def run_laplacian_coordinates(image_main, seeds, slide, view):
  print("laplacian_coordinates")
  if view == 'coronal':
    image = image_main[:, :, slide]
    seeds_img = seeds[:, :, slide]
  elif view == 'sagital':
    image = image_main[slide, :, :]
    seeds_img = seeds[slide, :, :]
  elif view == 'axial':
    image = image_main[:, slide, :]
    seeds_img = seeds[:, slide, :]
  
  seeds_background = np.array(np.where(seeds_img == 1)).T
  seeds_foreground = np.array(np.where(seeds_img == 2)).T
  
  # print(image.shape, view, slide)
  # print(seeds_background)
  # print(seeds_foreground)
  
  matriz_adyacencia = ecuacion1(image, 1)
  pesos_di = array_di(matriz_adyacencia, image.shape)
  x_result = solve_linear_system(pesos_di, matriz_adyacencia, image, seeds_background, seeds_foreground)
  new_img = etiquetado_final(image, x_result, seeds_background, seeds_foreground)
  
  print("Fin laplacian_coordinates")
  
  return new_img