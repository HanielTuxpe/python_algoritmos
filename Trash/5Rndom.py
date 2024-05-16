import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import random as rd

class Poblacion:
    
    def __init__(self, NP, Dim, seed=None):
        self.NP = NP
        self.Dim = Dim
        self.seed = seed
        self.MAX = 100
        self.MIN = -100
        self.individuos = self.generar_poblacion(seed)
        self.o = np.random.uniform(low=-80, high=80, size=self.Dim)
        
    def generar_poblacion(self, seed):
        if seed is not None:
            np.random.seed(seed)
        return [self.generar_individuo(self.Dim) for _ in range(self.NP)]
    
    def generar_individuo(self, Dim):
        return np.random.uniform(low=-100, high=100, size=Dim)

    def evaluar_individuo(self, individuo):
        z = individuo - self.o
        F5 = -1000
        suma = 0
        for j in range(self.Dim):
            suma += abs(z[j]) ** (2 + 4 * (j / (self.Dim - 1)))
        resultado = math.sqrt(suma) - F5
        return resultado
    
    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar_individuo(individuo) for individuo in self.individuos]
        return evaluaciones

    def restriccion(self, valores):
        for i in range(len(valores)):
            if valores[i] > self.MAX or valores[i] < self.MIN:
                valores[i] = self.MIN + rd.random() * (self.MAX - self.MIN)
        return valores

    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        return nuevo_individuo

    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        hijo = self.restriccion(hijo)
        return hijo

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
    seed = int(datetime.now().timestamp())
    poblacion = Poblacion(NP, D, seed)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    fitness_Gen = []
    
    for i in range(max_gen):
        poblacion.seleccion(CR, F)
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        
        fitness_Gen.append(mejor_evaluacion)
    
    print("Fitness general:")
    for i in range(len(fitness_Gen)):
        print(f"Generación {i + 1}: {fitness_Gen[i]}")
    
    plt.plot(range(len(fitness_Gen)), fitness_Gen, marker='o', linestyle='-')
    plt.xlabel('Generación')
    plt.ylabel('Mejor Fitness')
    plt.title('Convergencia del Algoritmo Evolucion Diferencial-Random')
    plt.show()
    
    print("Mejor individuo encontrado:")
    print(mejor_individuo)
    print("Mejor evaluación:")
    print(mejor_evaluacion)

NP = 100
CR = 0.7
F = 0.6
D = 10
max_gen = 1000

algoritmo_evolutivo(NP, CR, F, max_gen, D)
