import copy
import numpy as np

def white_stripe(umbral, img_main):
    image = copy.deepcopy(img_main)
    # Calculamos el histograma de intensidades
    hist, bins = np.histogram(
        image.flatten(), bins=256, range=[0, np.max(image)])

    # Calculamos la derivada del histograma
    deriv = np.diff(hist)

    # Buscamos los máximos locales en el histograma. Estos corresponden a los picos.
    maximos = []
    for i in range(1, len(hist)-1):
        if hist[i-1] < hist[i] > hist[i+1] and hist[i] > umbral:
            maximos.append(i)

    ultimo_pico = maximos[-1]

    # Estandarizacion
    ws = bins[ultimo_pico]
    print('Ultimo pico:', ws)
    new_image = image/ws
    print("Fin de white_space!!!")
    return new_image