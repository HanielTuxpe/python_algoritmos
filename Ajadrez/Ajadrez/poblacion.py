import numpy as np

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



def generaPoblacion(tamaño):
    poblacion = []  
    for _ in range(tamaño):  
        arreglo_unico = generarIndividuo()  
        poblacion.append(arreglo_unico) 
    return poblacion



for i, arreglo in enumerate(generaPoblacion(10)):
    print(f"Arreglo {i+1}: {arreglo}") 
