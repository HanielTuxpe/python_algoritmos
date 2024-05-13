import random 
import numpy as np

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


def seleccion_por_torneo(poblacion, tamano_torneo):
    seleccionados = []

    while len(seleccionados) < 1:
        # Seleccionamos un torneo aleatorio
        torneo_indices = np.random.choice(len(poblacion), size=tamano_torneo, replace=False)
        torneo = poblacion[torneo_indices]

        # Elegimos el individuo con el menor fitness en el torneo
        mejor_individuo = torneo[np.argmin(evaluar_poblacion(torneo))]

        seleccionados.append(mejor_individuo)

    return seleccionados[0]


def cruza(poblacion):
    
    poblacion_copy = poblacion.copy()
    # Creamos una lista para almacenar a los padres seleccionados
    ChildParents = []
    # Creamos una matriz para almacenar a los hijos
    childs = []
    
    # Creamos un conjunto para almacenar los índices de los padres seleccionados
    selected_indices = set()
    
    # Mientras no hayamos generado suficientes hijos
    while len(childs) < len(poblacion):

        # Seleccionamos dos padres unicos aleatoriamente
        firstParent_index = random.choice(range(len(poblacion_copy)))
        sec_index = random.choice(range(len(poblacion_copy)))
        while sec_index == firstParent_index or sec_index in selected_indices:
            sec_index = random.choice(range(len(poblacion_copy)))
        secondParent_index = sec_index
        
        # Guardamos los índices de los padres seleccionados
        selected_indices.add(firstParent_index)
        selected_indices.add(secondParent_index)
        
        firstParent = poblacion_copy[firstParent_index]
        secondParent = poblacion_copy[secondParent_index]
        
        ChildParents.append((firstParent, secondParent))

    # Generamos los hijos
    for parents in ChildParents:
        firstParent, secondParent = parents

        #Se crear los hijos tomando los primeros cuatro valor de cada padres y evaluando si no se encuentran en el otro padre para completar al hijo        
        firstChild = np.concatenate((firstParent[:4], [num for num in secondParent if num not in firstParent[:4]]))
        secondChild = np.concatenate((secondParent[:4], [num for num in firstParent if num not in secondParent[:4]]))
        
        #Se crea una nueva generacion de hijos 
        childs.append(firstChild)
        childs.append(secondChild)
        
    return childs