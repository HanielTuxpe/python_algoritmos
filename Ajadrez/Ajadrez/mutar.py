import random
import numpy as np
from evaluar import evaluar_poblacion

PORCENTAJE_MUTACION = 0.10

# Función para generar los índices que van a mutar en la población de hijos
def generar_indices(poblacion_hijos):
    # Calcula el número de hijos a mutar
    cantidad_de_hijos = int(PORCENTAJE_MUTACION * len(poblacion_hijos))

    # Genera índices aleatorios para mutar
    indices_a_mutar = random.sample(range(len(poblacion_hijos)), cantidad_de_hijos)

    return indices_a_mutar

# Función para realizar la mutación en la población de hijos
def mutar(poblacion_hijos):
    # Genera los índices de los hijos que se van a mutar
    indices_a_mutar = generar_indices(poblacion_hijos)

    print("Indices")
    print(indices_a_mutar)

    # Realiza la mutación en los hijos seleccionados
    for indice in indices_a_mutar:
        # Genera dos índices aleatorios distintos
        indice_1, indice_2 = random.sample(range(8), 2)
        print("Indices aletorios")
        print(indice_1, indice_2)

        # Intercambia los valores en las posiciones seleccionadas
        poblacion_hijos[indice, indice_1], poblacion_hijos[indice, indice_2] = poblacion_hijos[indice, indice_2], poblacion_hijos[indice, indice_1]

    return poblacion_hijos

#compara hijos y padres y selecciona a los mejores, los almacena en una matriz
def decendientes(poblacion_hijos, poblacion_padres):
    # Evaluar las poblaciones
    fitness_hijos = evaluar_poblacion(poblacion_hijos)
    fitness_padres = evaluar_poblacion(poblacion_padres)
    
    # Crear una matriz de descendencia del mismo tamaño que la población de hijos
    _decendientes = np.zeros_like(poblacion_hijos)
    
    # Iterar sobre los índices de los individuos
    for i in range(len(poblacion_hijos)):
        if fitness_hijos[i] < fitness_padres[i]:
            _decendientes[i] = poblacion_hijos[i]
        else:
            _decendientes[i] = poblacion_padres[i]
    return _decendientes

#######################################################################

#8.1.1 Mutacion por Insercion
def mutar_insercion(poblacion_hijos):
    # Genera los índices de los hijos que se van a mutar
    indices_a_mutar = generar_indices(poblacion_hijos)

    # print("Indices a mutar:")
    # print(indices_a_mutar)

    # Realiza la mutación en los hijos seleccionados
    for indice in indices_a_mutar:
        # Selecciona un valor aleatorio de la población hijo
        hijo = poblacion_hijos[indice]
        valor = np.random.choice(hijo)
        
        # Encuentra la posición del valor en el hijo
        posicion = np.where(hijo == valor)[0][0]
        
        # Elimina el valor de su posición original
        hijo = np.delete(hijo, posicion)
        
        # Selecciona una posición aleatoria para insertar el valor
        nueva_posicion = random.randint(0, len(hijo))
        
        # Inserta el valor en la nueva posición
        hijo = np.insert(hijo, nueva_posicion, valor)

        poblacion_hijos[indice] = hijo

    return poblacion_hijos

if __name__ == "__main__":
    poblacion_hijos = np.random.randint(8, size=(10, 8))
    poblacion_padres = np.random.randint(8, size=(10, 8))
    print("--------------------POBLACIONES------------------------")
    print(poblacion_hijos)
    print("--------------------------------------------")
    print(poblacion_padres)
    print("------------------MUTACIONES--------------------------")
    mutacion_hijos = mutar_insercion(poblacion_hijos)
    print(mutacion_hijos)
    print("------------------EVALUACION--------------------------")
    print(evaluar_poblacion(mutacion_hijos))
    print("--------------------------------------------")
    print(evaluar_poblacion(poblacion_padres))
    print("------------------DESENDENCIA--------------------------")
    print(decendientes(mutacion_hijos, poblacion_padres))