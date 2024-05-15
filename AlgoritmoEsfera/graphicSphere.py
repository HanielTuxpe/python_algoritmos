import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime

class Poblacion:
    
    def __init__(self, NP, Dim, seed=None):
        self.NP = NP
        self.Dim = Dim
        self.seed = seed
        self.individuos = self.generar_poblacion(seed)
        
    # Función para generar una población inicial de tamaño NP
    def generar_poblacion(self, seed):
        if seed is not None:
            np.random.seed(seed)
        return [self.generar_individuo(self.Dim) for _ in range(self.NP)]
    
    def generar_individuo(self, Dim):
        return np.random.uniform(low=-100, high=100, size=Dim)

    # Función para evaluar el individuo
    def evaluar_individuo(self, individuo):
        o = np.random.uniform(low=-80, high=80, size=10)
        z = individuo - o
        f_constante = -1400
        suma_cuadrados = np.sum(z**2)
        return suma_cuadrados + f_constante
    
    # Función para evaluar la función objetivo de toda la población
    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar_individuo(individuo) for individuo in self.individuos]
        return evaluaciones

    # Restricciones
    def rest_bou(self, valores):
        return np.clip(valores, -100, 100)

    def rest_reflex(self, valores, inf_lim, sup_lim):
        for i in range(len(valores)):
            if valores[i] < inf_lim[i]:
                valores[i] = 2 * inf_lim[i] - valores[i]
            elif valores[i] > sup_lim[i]:
                valores[i] = 2 * sup_lim[i] - valores[i]
        return valores

    # Función para realizar la mutación de un individuo
    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = individuo[j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        return nuevo_individuo

    # Función para realizar la cruz de dos individuos
    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        # Aplicar restricción por reflexión para asegurarse de que los valores estén dentro del rango [-100, 100]
        inf_lim = np.full_like(hijo, -100)
        sup_lim = np.full_like(hijo, 100)
        
        print(inf_lim, sup_lim)
        
        hijo = self.rest_reflex(hijo, inf_lim, sup_lim)
        return hijo

    # Función para realizar la selección de un individuo
    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            if self.evaluar_individuo(cruzado) <= evaluaciones[i]:
                nueva_poblacion.append(cruzado)
            else:
                nueva_poblacion.append(individuo)
        self.individuos = nueva_poblacion

def algoritmo_evolutivo(NP, CR, F, max_gen, D):
    seed = int(datetime.now().timestamp())  # Generar una semilla aleatoria basada en el tiempo actual
    poblacion = Poblacion(NP, D, seed)  # Generar población aleatoria con la semilla
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    fitness_Gen = []
    
    for i in range(max_gen):
        poblacion.seleccion(CR, F)  # Seleccionar, Mutar y Cruzar
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        
        # Evaluar el trial
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
            
            # Añadir si es menor y no está en el array
            if mejor_evaluacion not in fitness_Gen:
                fitness_Gen.append(mejor_evaluacion)
        
        print(f"Best Ind Gen {i} : {mejor_individuo}")
        
    # Añadir el mejor individuo encontrado
    print("fitness general")
    for i in range(len(fitness_Gen)):
        print(fitness_Gen[i])
    
    # Graficar la convergencia
    plt.plot(range(len(fitness_Gen)), fitness_Gen, marker='o', linestyle='-')
    plt.xlabel('Generación')
    plt.ylabel('Mejor Fitness')
    plt.title('Convergencia del Algoritmo Evolutivo')
    plt.show()

# Parámetros del algoritmo
NP = 10
CR = 0.9
F = 0.9
D = 10
max_gen = 50

# Llamar a la función principal
algoritmo_evolutivo(NP, CR, F, max_gen, D)