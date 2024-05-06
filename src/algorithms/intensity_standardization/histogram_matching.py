import copy
import numpy as np
import scipy.stats as sp

def def_lambda (m,b):
  return lambda x: (m*x) + b

def training(inputData, k):
  print("training...")
  x = np.linspace(5,95,k)
  y = np.percentile(inputData.flatten(), x)

  functions = []

  for i in range(k):
    if (i+1 < k):
      m = (y[i+1] - y[i]) / (x[i+1] - x[i])
      b = y[i] - m*x[i]
      fn = lambda x: m*x + b
      functions.append(def_lambda(m,b))

  return functions

# Landmark: x en la anterior, son percentiles
def testing(inputData, functions, landmark, k):
  print("testing...")
  percentil = sp.percentileofscore(sorted(list(set(inputData.flatten())), reverse = False), inputData)

  new_image = np.zeros(inputData.shape)
  for i in range(k):
    if (i+1 < k):
      new_image[(percentil > landmark[i]) & (percentil < landmark[i+1])] = functions[i](percentil[(percentil > landmark[i]) & (percentil < landmark[i+1])])

  return new_image

def histogram_matching(trainData, testData, k):
  x = np.linspace(5,95,k)
  y = np.percentile(trainData.flatten(), x)

  train_functions = training(trainData, k)
  new_img = testing(testData, train_functions, y, k)
  print('Fin histogram matching!!!')

  return new_img