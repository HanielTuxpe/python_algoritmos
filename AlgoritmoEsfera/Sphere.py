import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    # Función para generar una población inicial de tamaño NP
    def generar_individuo(self):
        return np.random.uniform(low=-100, high=100, size=10)

    # Función para evaluar el individuo
    def evaluar_individuo(self, individuo):
        # Calcular z, la diferencia entre x y o
        o = np.random.uniform(low=-80, high=80, size=10)
        z = individuo - o
        f_constante = -1400
        # Calcular la suma del cuadrado de cada componente de z
        suma_cuadrados = np.sum(z**2)
        # Sumar el resultado con f_constante
        return suma_cuadrados + f_constante
    
    # Función para evaluar la función objetivo de toda la población
    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar_individuo(individuo) for individuo in self.individuos]
        return evaluaciones

    # Función para realizar la mutación de un individuo
    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = individuo[j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        return nuevo_individuo

    def rest_bou(self, valores):
        return np.clip(valores, -100, 100)

    def rest_reflex(self, valores, inf_lim, sup_lim):
        for i in range(len(valores)):
            if valores[i] < inf_lim[i]:
                valores[i] = 2 * inf_lim[i] - valores[i]
            elif valores[i] > sup_lim[i]:
                valores[i] = 2 * sup_lim[i] - valores[i]
        return valores

    # Función para realizar la cruz de dos individuos
    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        # Aplicar restricción por reflexión para asegurarse de que los valores estén dentro del rango [-100, 100]
        inf_lim = np.full_like(hijo, -100)
        sup_lim = np.full_like(hijo, 100)
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

def algoritmo_evolutivo(NP, CR, F, max_gen):
    poblacion = Poblacion(NP) #Generar población aleatoria
    print(f"Población Inicial:")
    for individuo in poblacion.individuos:
        print(individuo)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    
    for i in range(max_gen):
        poblacion.seleccion(CR, F) # Seleccionar, Mutar y Cruzar
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        
        # Evaluar el trial
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        
        print(f"Generación {i+1}:")
        for individuo in poblacion.individuos:
            print(individuo)
        
        print(f"Generación {i+1}:")
        print(individuo)
        
    print("Mejor individuo:", mejor_individuo)
    print("Mejor evaluación:", mejor_evaluacion)
    # Añadir el mejor individuo encontrado

NP = 50
CR = 0.9
F = 0.9
max_gen = 100
algoritmo_evolutivo(NP, CR, F, max_gen)
