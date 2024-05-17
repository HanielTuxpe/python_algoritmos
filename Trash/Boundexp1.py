import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

final_fit = []

class DifEvo_Bound:
    
    def __init__(self, NP, Dim, seed=None):
        self.NP = NP
        self.Dim = Dim
        self.seed = seed
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
        f_constante = -1400
        suma_cuadrados = np.sum(z**2)
        fitness = suma_cuadrados - f_constante
        return fitness
    
    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar_individuo(individuo) for individuo in self.individuos]
        return evaluaciones

    def rest_bou(self, valores):
        return np.clip(valores, -100, 100)

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
        hijo = self.rest_bou(hijo)
        return hijo

    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            if self.evaluar_individuo(cruzado) < evaluaciones[i]:
                nueva_poblacion.append(cruzado)
            else:
                nueva_poblacion.append(individuo)
        self.individuos = nueva_poblacion


def algoritmo_evolutivo(NP, CR, F, max_gen, D):
    seed = int(datetime.now().timestamp())
    poblacion = DifEvo_Bound(NP, D, seed)
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
    
    return mejor_evaluacion
    
    plt.plot(range(len(fitness_Gen)), fitness_Gen,  marker='o')
    plt.xlabel('Generación')
    plt.ylabel('Mejor Fitness')
    plt.title('Convergencia del Algoritmo Evolución Diferencial: Esfera/Bounds')
    plt.show()

def main():
    NP = 100
    CR = 0.7
    F = 0.6
    D = 10
    max_gen = 1000

    for i in range (25):
        print(f"vuelta {i}")
        min_fit = algoritmo_evolutivo(NP, CR, F, max_gen, D)
        final_fit.append(min_fit)
        
    return final_fit

if __name__ == '__main__':
    fitness= main()
    print(fitness)