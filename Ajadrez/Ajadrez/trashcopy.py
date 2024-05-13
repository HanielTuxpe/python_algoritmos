import random 
import numpy as np
fitness = []
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


""" SELECCION POR TORNEO """

def seleccion_por_torneo(poblacion, tamano_torneo):
    while True:
        # Seleccionamos un torneo aleatorio
        torneo_indices = np.random.choice(len(poblacion), size=tamano_torneo, replace=False)
        torneo = poblacion[torneo_indices]

        # Elegimos el índice del individuo con el menor fitness en el torneo
        indice_mejor_individuo = torneo_indices[np.argmin(evaluar_poblacion(torneo))]

        return indice_mejor_individuo



""" SELECCION POR JERARQUIA """
def calcular_jerarquia(poblacion):
    jerarquia = np.zeros(len(poblacion), dtype=int)
    for i in range(len(poblacion)):
        choques = evaluar_choques(poblacion[i])
        jerarquia[i] = choques
    return jerarquia

def calcular_probabilidades_seleccion(jerarquia):
    total_jerarquias = sum(jerarquia)
    probabilidades = [jerarquia[i] / total_jerarquias for i in range(len(jerarquia))]
    return probabilidades

def seleccion_por_jerar(poblacion, probabilidades):
    indice_seleccionado = np.random.choice(len(poblacion), p=probabilidades)
    return indice_seleccionado

def ordenar_poblacion(poblacion):
    fitness = evaluar_poblacion(poblacion)
    indices_ordenados = np.argsort(fitness)
    poblacion_ordenada = [poblacion[i] for i in indices_ordenados]
    return poblacion_ordenada

def seleccion_por_jerarquia(poblacion):
    jerarquia = calcular_jerarquia(poblacion)
    probabilidades = calcular_probabilidades_seleccion(jerarquia)
    individuo_seleccionado = seleccion_por_jerar(poblacion, probabilidades)
    return individuo_seleccionado
""" CRUZA """

def cruza_order_based(poblacion, tamano_torneo):
    poblacion_copy = poblacion.copy()
    childs = []
    selected_indices = []

    while len(childs) < len(poblacion):
        # Seleccionamos el primer padre mediante torneo
        firstParent_index = seleccion_por_torneo(poblacion_copy, tamano_torneo)
        
        # Seleccionamos el segundo padre mediante jerarquía de la población original
        secondParent_index = seleccion_por_jerarquia(poblacion)
        
        # Verificamos que no se hayan seleccionado previamente los padres
        if firstParent_index in selected_indices or secondParent_index is None:
            continue

        # Almacenamos los índices de los padres seleccionados
        selected_indices.append(firstParent_index)
        selected_indices.append(secondParent_index)

        firstParent = poblacion_copy[firstParent_index]
        secondParent = poblacion[secondParent_index]
        
        # No necesitamos eliminar al segundo padre de la población copia, simplemente lo ignoramos durante la selección

        # Elegimos los valores de P1
        p1_values = np.random.choice(firstParent, size=np.random.randint(1, len(firstParent)), replace=False)

        # Creamos P2' eliminando los valores de P1 de P2
        p2_prime = [num if num not in p1_values else 'X' for num in secondParent]

        # Generamos el primer hijo a partir de P2'
        child1 = ['X' if num == 'X' else num for num in p2_prime]

        # Insertamos la secuencia elegida de P1 en el primer hijo
        p1_index = 0
        for i in range(len(child1)):
            if child1[i] == 'X':
                child1[i] = p1_values[p1_index]
                p1_index += 1

        childs.append(child1)

        # Generamos el segundo hijo intercambiando los padres
        p1_values = np.random.choice(secondParent, size=np.random.randint(1, len(secondParent)), replace=False)
        p2_prime = [num if num not in p1_values else 'X' for num in firstParent]
        child2 = ['X' if num == 'X' else num for num in p2_prime]
        p1_index = 0
        for i in range(len(child2)):
            if child2[i] == 'X':
                child2[i] = p1_values[p1_index]
                p1_index += 1

        childs.append(child2)

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
def main():
    poblacion_actual = generaPoblacion(20)
    generaciones = 0
    
    while generaciones < 10:
        descendientes_generados = cruza_order_based(poblacion_actual, 3)
        descendientes_mutados = mutar(np.array(descendientes_generados))
        poblacion_actual = decendientes(descendientes_mutados, poblacion_actual)
        generaciones += 1
        
        # Evaluar si hay un individuo con fitness 0
        fitness_poblacion = evaluar_poblacion(poblacion_actual)
        min_fitness_index = np.argmin(fitness_poblacion)
        min_fitness = fitness_poblacion[min_fitness_index]

        print(f"Generación {generaciones}:")
        if min_fitness == 0:
            print(f"Se encontró un individuo con fitness 0 en la generación {generaciones}: {poblacion_actual[min_fitness_index]}")
            fitness.append(min_fitness)
            return
        print(f"Fitness más bajo: {min_fitness}, Individuo: {poblacion_actual[min_fitness_index]}")
        
    else:
        print("Se completaron 30 generaciones sin encontrar un individuo con fitness 0.")
        fitness.append(min_fitness)

    return fitness

if __name__== "__main__":
    for _ in range(25):
        main()
    

    print(fitness)
