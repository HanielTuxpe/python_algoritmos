import numpy as np

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    # Función para generar una población inicial de tamaño NP
    def generar_individuo(self):
        return np.random.uniform(low=-20, high=20, size=2)

    # Función para evaluar la función objetivo de un individuo
    def evaluar(self, individuo):
        x1, x2 = individuo
        # Función de aptitud: f(x1, x2) = (x1^3 + x2^3 )/ 100
        return (x1**3 + x2**3) / 100

    # Función para evaluar la función objetivo de toda la población
    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar(individuo) for individuo in self.individuos]
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

    # Función para realizar la cruz de dos individuos
    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        # Aplicar restricción para asegurarse de que los valores estén dentro del rango [-20, 20]
        hijo = np.clip(hijo, -20, 20)
        return hijo

    # Función para realizar la selección de un individuo
    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            if self.evaluar(cruzado) <= evaluaciones[i]:
                nueva_poblacion.append(cruzado)
            else:
                nueva_poblacion.append(individuo)
        self.individuos = nueva_poblacion

def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = Poblacion(NP) #Generar población aleatoria
    print("Población inicial:")
    for individuo in poblacion.individuos:
        print(individuo)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F) #Seleccionar, Mutar y Cruzar
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        #Evaluar el trial
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        print(f"Generación {i+1}:")
        for individuo in poblacion.individuos:
            print(individuo)
    return mejor_individuo, mejor_evaluacion


NP = 10
CR = 0.9
F = 0.9
max_generaciones = 100
mejor_individuo, mejor_evaluacion = algoritmo_evolutivo(NP, CR, F, max_generaciones)
print("Mejor individuo:", mejor_individuo)
print("Mejor evaluación:", mejor_evaluacion)
