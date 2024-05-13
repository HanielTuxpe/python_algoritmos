import numpy as np
# Función para evaluar el número de choques en un individuo 
def evaluar_choques(individuo):
    # Inicializamos el contador de choques
    choques = 0
    # Iteramos sobre todas las reinas
    for i in range(8):
        # Iteramos sobre las reinas restantes
        for j in range(i+1, 8):
            # Verificamos si hay choques en diagonales
            if abs(individuo[i] - individuo[j]) == abs(i - j):
                choques += 2
    # Devolvemos el número total de choques
    return choques

# Función para evaluar el fitness de una población de individuos
def evaluar_poblacion(poblacion):
    # Calculamos el número de individuos en la población
    n = len(poblacion)
    # Creamos un arreglo para almacenar el fitness de cada individuo en la población
    fitness = np.zeros(n, dtype=int)
    # Iteramos sobre cada individuo en la población
    for i in range(n):
        # Calculamos el número de choques en el individuo actual
        choques = evaluar_choques(poblacion[i])
        # Asignamos el número de choques al arreglo de fitness
        fitness[i] = choques
    # Devolvemos el arreglo de fitness de la población
    return fitness


    
