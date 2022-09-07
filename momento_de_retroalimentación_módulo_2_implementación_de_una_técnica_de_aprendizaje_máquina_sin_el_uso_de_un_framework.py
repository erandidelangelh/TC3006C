# -*- coding: utf-8 -*-
"""Momento de Retroalimentación: Módulo 2 Implementación de una técnica de aprendizaje máquina sin el uso de un framework

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10wmOFT4xMoGVqcDwdqYWGXFAVB2LL4a5

# Librerías
"""

import pandas as pd
from google.colab import drive
import matplotlib.pyplot as plt
import numpy as np

"""# Divisón del data set en entrenamiento y prueba"""

# Función que divide los datasets en entrenamiento y prueba
import random

def split_dataset(porcentaje, dataset):

  columna0 = dataset.columns[0]
  columna1 = dataset.columns[1]
  X = dataset[columna0].values
  Y = dataset[columna1].values

  cantidad = int((len(X) * porcentaje) / 100)
  lst = list(range(0,len(X)))
  arr_train_X = np.array([])
  arr_train_Y = np.array([])

  for i in range(0, cantidad):
    indice = random.choice(lst)

    # Creación de DataFrame de entrenamiento de X
    arr_train_X = np.append(arr_train_X, X[indice])
    train_X = pd.DataFrame(arr_train_X, columns = [columna0])

    # Creación de DataFrame de entrenamiento de Y
    arr_train_Y = np.append(arr_train_Y, Y[indice])
    train_Y = pd.DataFrame(arr_train_Y, columns = [columna1])

    lst.remove(indice)

  test_X = pd.DataFrame(X[lst], columns = [columna0])
  test_Y = pd.DataFrame(Y[lst], columns = [columna1])

  return train_X, train_Y, test_X, test_Y

"""# Construcción de modelo de regresión

𝐲 = β1*x + β0

## Fit del modelo
"""

def fit(dataset_X, dataset_Y):

  columna0 = dataset_X.columns[0]
  columna1 = dataset_Y.columns[0]
  X = dataset_X[columna0].values
  Y = dataset_Y[columna1].values

  # Cálculo de los coeficientes
  suma_x = X.sum()
  suma_y = Y.sum()

  suma_xy = (X*Y).sum()

  suma_x2 = (X**2).sum()
  suma_y2 = (Y**2).sum()

  promedio_x = np.mean(X)
  promedio_y = np.mean(Y)

  n = len(X)

  b0 = (suma_y*suma_x2 - suma_x*suma_xy) / (n*suma_x2 - (suma_x**2))
  b1 = (n*suma_xy - suma_x*suma_y) / (n*suma_x2 - (suma_x)**2)
  coeficientes = [b0, b1]
  train_y = b1*X + b0

  return X, Y, coeficientes, train_y

"""## Entrenamiento"""

def regresion(dataset_X, dataset_Y, fit):
  X, Y, coeficientes, train_y = fit

  X_test = dataset_X[dataset_X.columns[0]].values
  Y_test = dataset_Y[dataset_Y.columns[0]].values
  
  test_y = coeficientes[1]*X_test + coeficientes[0]
  resultado = pd.DataFrame({test_X.columns[0] : test_X.iloc[:, 0], test_Y.columns[0]: test_Y.iloc[:, 0], 'Predicción '+ test_Y.columns[0]: test_y})

  return test_y, resultado

"""# Evaluación"""

# Mean Squared Error, Mean Absolute Error, Root Mean Squared Error, Mean Percent Absolute Error, Sum of Squared Errors, Coeficiente de determinación
def evaluacion(resultado):
  n = len(resultado)
  resultado['Error'] = resultado.iloc[:,1] - resultado.iloc[:,2]
  resultado['Error Absoluto'] = abs(resultado.iloc[:,1] - resultado.iloc[:,2])
  resultado['Squared Error'] = (resultado.iloc[:,1] - resultado.iloc[:,2])**2
  media_y = resultado.iloc[:,1].mean()

  SSE = resultado['Squared Error'].sum()
  MSE = SSE / n
  MAE = resultado['Error Absoluto'].sum() / n
  RMSE = MSE**(1/2)
  MAPE = (abs(resultado['Error']/resultado.iloc[:,1]).sum()) / n
  R2 = (((resultado.iloc[:,2] - media_y)**2).sum()) / (((resultado.iloc[:,1] - media_y)**2).sum())

  print('Mean Squared Error: ', MSE)
  print('Mean Absolute Error: ', MAE)
  print('Root Mean Squared Error', RMSE)
  print('Mean Percent Absolute Error', MAPE)
  print('Sum of Squared Errors', SSE)
  print('Coeficiente de determinación', R2)

  return resultado, MSE, MAE, RMSE, MAPE, SSE, R2

"""# Cargar datos

Se obtienen los datos de Google Drive
"""

drive.mount("/content/gdrive")

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/gdrive/MyDrive/Colab Notebooks/Concentración 7to/Uresti"
!ls

datos = pd.read_csv('income.data.csv')
datos.drop(['Unnamed: 0'], axis=1, inplace=True)
datos

"""# Pruebas"""

# Prueba 1
train_X, train_Y, test_X, test_Y = split_dataset(70, datos) # División de dataset de prueba y entrenamiento
test_y, resultado = regresion(test_X, test_Y, fit(train_X, train_Y))   # Predicción de y del dataset de prueba
resultado, MSE, MAE, RMSE, MAPE, SSE, R2 = evaluacion(resultado)
resultado

"""En la segunda prueba se modificó el tamaño de los dataset de entrenamiento y prueba y el resultado fue que los valores de los errores disminuyó"""

# Prueba 2
train_X, train_Y, test_X, test_Y = split_dataset(90, datos) # División de dataset de prueba y entrenamiento
test_y, resultado = regresion(test_X, test_Y, fit(train_X, train_Y))   # Predicción de y del dataset de prueba
resultado, MSE, MAE, RMSE, MAPE, SSE, R2 = evaluacion(resultado)
resultado.head()

