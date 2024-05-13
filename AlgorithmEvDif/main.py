import random 
import numpy as np

""" POBLACIÓN """ 
def generarRandom():
    array = np.random.uniform(-20, 20, size=2)
    np.random.shuffle(array)
    return array


def generaPoblacion(tamano):
    poblacion = []  
    for _ in range(tamano):  
        arreglo_unico = generarRandom()  
        poblacion.append(arreglo_unico) 
    return np.array(poblacion)

""" EVALUAR """
#Función para evaluar el número de choques en un individuo 
def evaluar_aptitud(individuo):
    x1, x2 = individuo
    # Función de aptitud: f(x1, x2) = (x1^3 + x2^3 )/ 100
    return (x1**3 + x2**3) /100


# Función para evaluar el fitness de una población de individuos
def evaluar_poblacion(poblacion):
    # Calculamos el número de individuos en la población
    n = len(poblacion)
    # Creamos un arreglo para almacenar el fitness de cada individuo en la población
    fitness = np.zeros(n, dtype=float)
    # Iteramos sobre cada individuo en la población
    for i in range(n):
        # Calculamos el número de choques en el individuo actual
        aptitud = evaluar_aptitud(poblacion[i])
        # Asignamos el número de choques al arreglo de fitness
        fitness[i] = aptitud
    # Devolvemos el arreglo de fitness de la población
    return fitness

def mutacion(poblacion, f):
    # Crear un arreglo para almacenar la población mutada
    poblacion_mutada = np.zeros_like(poblacion)
    # Iterar sobre cada individuo en la población
    for i in range(len(poblacion)):
        # Seleccionar tres índices únicos aleatorios
        indices = random.sample(range(len(poblacion)), 3)
        # Seleccionar tres soluciones aleatorias
        a, b, c = poblacion[indices]
        # Mutación de diferencia
        mutacion = a + f * (b - c)
        # Almacenar la solución mutada en el arreglo de población mutada
        poblacion_mutada[i] = mutacion
    return poblacion_mutada

# Función de cruza

import numpy as np
import random

def cruza(poblacion, poblacion_mutada, cr):
    # Definir los límites
    limite_inferior = -20
    limite_superior = 20
    
    # Obtener el tamaño de la población
    n = len(poblacion)
    # Crear un arreglo para almacenar la población cruzada
    poblacion_cruzada = np.zeros_like(poblacion)
    # Iterar sobre cada individuo en la población
    for i in range(n):
        # Crear un nuevo individuo cruzado
        cruzada = np.zeros_like(poblacion[i])
        # Seleccionar un índice aleatorio para la cruza
        j_rand = random.randint(0, len(poblacion[i]) - 1)
        # Iterar sobre cada gen en el individuo
        for j in range(len(poblacion[i])):
            # Aplicar la operación de cruza binomial
            if random.random() < cr or j == j_rand:
                cruzada[j] = poblacion_mutada[i][j]
            else:
                cruzada[j] = poblacion[i][j]
            # Manejo de restricciones de límite
            if cruzada[j] > limite_superior:
                cruzada[j] = limite_superior
            elif cruzada[j] < limite_inferior:
                cruzada[j] = limite_inferior
        # Almacenar el individuo cruzado en el arreglo de población cruzada
        poblacion_cruzada[i] = cruzada
    return poblacion_cruzada


# Número de generaciones
cant_generaciones = 30

# Población inicial
poblacion = generaPoblacion(10)
print(poblacion)

# Evolución a lo largo de las generaciones
for generacion in range(cant_generaciones):
    # Evaluación de la población actual
    fitness = evaluar_poblacion(poblacion)
    
    # Seleccionar el mejor individuo de la generación actual
    mejor_individuo = poblacion[np.argmax(fitness)]
    
    # Imprimir el mejor individuo de la generación actual
    #print(f"Generación {generacion + 1} - Mejor individuo: {mejor_individuo} - Fitness: {max(fitness)}")
    
    # Aplicar mutación y cruce
    poblacion_mutada = mutacion(poblacion, 0.9)
    poblacion_cruzada = cruza(poblacion, poblacion_mutada, 0.9)
    
    # Reemplazar la población actual por la población cruzada
    poblacion = poblacion_cruzada

# Evaluar la población final
fitness_final = evaluar_poblacion(poblacion)
# Obtener el mejor individuo de la población final
mejor_individuo_final = poblacion[np.argmax(fitness_final)]
# Imprimir el mejor individuo de la población final
print("\nPoblación final:")
print(f"Mejor individuo final: {mejor_individuo_final} - Fitness final: {max(fitness_final)}")
