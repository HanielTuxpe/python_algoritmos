import random 
import numpy as np

_fitness = []
cant_generaciones = 10

""" POBLACIÓN """ 
def generarRandom():
    array= np.arange(8)
    np.random.shuffle(array)
    return array 
    

def generarIndividuo():
    individuo=generarRandom()
    for i, valor in enumerate(individuo):
        while i == valor:
            np.random.shuffle(individuo)
            valor = individuo[i]
    return individuo



def generaPoblacion(tamano):
    poblacion = []  
    for _ in range(tamano):  
        arreglo_unico = generarIndividuo()  
        poblacion.append(arreglo_unico) 
    return np.array(poblacion)



# for i, arreglo in enumerate(generaPoblacion(10)):
#     print(f"Arreglo {i+1}: {arreglo}") 

""" EVALUAR """
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

# print (evaluar_poblacion(generaPoblacion(10)))


""" CRUZA """
# def cruza(poblacion):
#     print(type(poblacion))
#     poblacion_copy = poblacion.copy()
#     # Creamos una lista para almacenar a los padres seleccionados
#     ChildParents = []
#     # Creamos una matriz para almacenar a los hijos
#     childs = []

#     # Mientras no hayamos generado suficientes hijos
#     while len(poblacion_copy) >= 2:


#         # Seleccionamos dos padres unicos aleatoriamente
#         firstParent = random.choice(poblacion_copy)
#         sec = random.choice(poblacion_copy)
#         while np.array_equal(sec, firstParent):
#             sec = random.choice(poblacion_copy)
#         secondParent = sec
        
#         # print(secondParent, firstParent)
        
#         ChildParents.append((firstParent, secondParent))

#         # Eliminamos los padres seleccionados de la lista poblacion_copy para ir dismuyendo y evitar que se repitan al seleccionarse nuevos
#         for parent in (firstParent, secondParent):
#             for ind, ind_copy in enumerate(poblacion_copy):
#                 if np.array_equal(ind_copy, parent):
#                     del poblacion_copy[ind]
#                     break
            
#     # Generamos los hijos
#     for parents in ChildParents:
#         firstParent, secondParent = parents

#         #Se crear los hijos tomando los primeros cuatro valor de cada padres y evaluando si no se encuentran en el otro padre para completar al hijo        
#         firstChild = np.concatenate((firstParent[:4], [num for num in secondParent if num not in firstParent[:4]]))
#         secondChild = np.concatenate((secondParent[:4], [num for num in firstParent if num not in secondParent[:4]]))
        
#         #Se crea una nueva generacion de hijos 
#         childs.append(firstChild)
#         childs.append(secondChild)
        
#     return childs
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
            
            ChildParents = []
        
    return childs


""" MUTACIÓN """

PORCENTAJE_MUTACION = 0.10

# Función para generar los índices que van a mutar en la población de hijos
def generar_indices(poblacion_hijos):
    # Calcula el número de hijos a mutar
    cantidad_de_hijos = int(PORCENTAJE_MUTACION * len(poblacion_hijos))

    # Genera índices aleatorios para mutar
    indices_a_mutar = random.sample(range(len(poblacion_hijos)), cantidad_de_hijos)

    return indices_a_mutar

# Funcion para realizar la mutacion en la poblacion de hijos
#8.1.3 Mutacion por Intercambio Reciproco//////////////////
def mutar(poblacion_hijos):
    # Genera los indices de los hijos que se van a mutar
    indices_a_mutar = generar_indices(poblacion_hijos)

    # print("Indices")
    # print(indices_a_mutar)

    # Realiza la mutacion en los hijos seleccionados
    for indice in indices_a_mutar:
        # Genera dos indices aleatorios distintos
        indice_1, indice_2 = random.sample(range(8), 2)
        # print("Indices aletorios")
        # print(indice_1, indice_2)

        # Intercambia los valores en las posiciones seleccionadas
        poblacion_hijos[indice, indice_1], poblacion_hijos[indice, indice_2] = poblacion_hijos[indice, indice_2], poblacion_hijos[indice, indice_1]

    return poblacion_hijos


""" DECENDENCIA """
#compara hijos y padres y selecciona a los mejores, los almacena en una matriz
def decendientes(poblacion_hijos, poblacion_padres):
    # Evaluar las poblaciones
    fitness_hijos = evaluar_poblacion(poblacion_hijos)
    fitness_padres = evaluar_poblacion(poblacion_padres)
    
    # Crear una matriz de descendencia del mismo tamano que la población de hijos
    _decendientes = np.zeros_like(poblacion_hijos)
    
    # Iterar sobre los índices de los individuos
    for i in range(len(poblacion_hijos)):
        if fitness_hijos[i] < fitness_padres[i]:
            _decendientes[i] = poblacion_hijos[i]
        else:
            _decendientes[i] = poblacion_padres[i]
    return _decendientes




""" GENREACION """
def _main():
    poblacion_actual = generaPoblacion(20)
    generaciones = 0

    try:
        while generaciones < cant_generaciones:
            descendientes_generados = cruza(poblacion_actual)
            descendientes_mutados = mutar(np.array(descendientes_generados))
            poblacion_actual = decendientes(descendientes_mutados, poblacion_actual)
            generaciones += 1
        
            # Evaluar si hay un individuo con fitness 0
            fitness_poblacion = evaluar_poblacion(poblacion_actual)
            min_fitness_index = np.argmin(fitness_poblacion)
            min_fitness = fitness_poblacion[min_fitness_index]
            print(f"Generación {generaciones}:")
            for i, fitness in enumerate(fitness_poblacion):
                if fitness == 0:
                    print(f"Se encontro un individuo con fitness 0 en la generacion {generaciones}: {poblacion_actual[min_fitness_index]}")
                    _fitness.append(min_fitness)
                    return
            print(f"Fitness más bajo: {min_fitness}, Individuo: {poblacion_actual[min_fitness_index]}")
        else:
            print(f"Se completaron {cant_generaciones} generaciones sin encontrar un individuo con fitness 0.")
            _fitness.append(min_fitness)
    except Exception as e:
        print(e)

    return _fitness
