import numpy as np

final_fit = []

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    # Función para generar una población inicial de tamaño NP
    def generar_individuo(self):
        individuo = np.zeros(13)
        individuo[:4] = np.random.uniform(low=0, high=1, size=4)
        individuo[4:9] = np.random.uniform(low=0, high=1, size=5)
        individuo[9:12] = np.random.uniform(low=0, high=10, size=3)  # Adjust the range
        individuo[12] = np.random.uniform(low=0, high=1)
        return individuo


    # Función para evaluar la función objetivo de un individuo
    def evaluar(self, individuo):
        x = individuo
        fitness = 5 * np.sum(x[:4]) - 5 * np.sum(x[:4]**2) - np.sum(x[4:])
        restricciones = self.evaluar_restricciones(individuo)
        penalizacion = sum([max(0, r) for r in restricciones])
        fitness += penalizacion * 10000  # Increase penalty factor
        return fitness, penalizacion


    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar(individuo) for individuo in self.individuos]
        return evaluaciones

    # Función para evaluar las restricciones
    def evaluar_restricciones(self, individuo):
        x = individuo
        restricciones = [
            2*x[0] + 2*x[1] + x[9] + x[10] - 10,
            2*x[0] + 2*x[2] + x[9] + x[11] - 10,
            2*x[1] + 2*x[2] + x[10] + x[11] - 10,
            -8*x[0] + x[9],
            -8*x[1] + x[10],
            -8*x[2] + x[11],
            -2*x[3] - x[4] + x[9],
            -2*x[5] - x[6] + x[10],
            -2*x[7] - x[8] + x[11]
        ]
        return restricciones

    # Función para evaluar si un individuo cumple con las restricciones
    def cumple_restricciones(self, individuo):
        restricciones = self.evaluar_restricciones(individuo)
        return all(r <= 0 for r in restricciones)

    # Función para realizar la mutación de un individuo
    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        # Aplicar límites a los genes
        nuevo_individuo[:9] = np.clip(nuevo_individuo[:9], 0, 1)
        nuevo_individuo[9:12] = np.clip(nuevo_individuo[9:12], 0, 100)
        nuevo_individuo[12] = np.clip(nuevo_individuo[12], 0, 1)
        return nuevo_individuo

    # Función para realizar la cruz de dos individuos
    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        # Aplicar límites a los genes
        hijo[:9] = np.clip(hijo[:9], 0, 1)
        hijo[9:12] = np.clip(hijo[9:12], 0, 100)
        hijo[12] = np.clip(hijo[12], 0, 1)
        return hijo

    # Función para realizar la selección de un individuo
    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            eval_cruzado, pen_cruzado = self.evaluar(cruzado)
            eval_individuo, pen_individuo = evaluaciones[i]
            
            # Always prefer feasible solutions
            if pen_cruzado == 0 and pen_individuo > 0:
                nueva_poblacion.append(cruzado)
            elif pen_cruzado > 0 and pen_individuo == 0:
                nueva_poblacion.append(individuo)
            elif pen_cruzado == 0 and pen_individuo == 0:
                if eval_cruzado < eval_individuo:
                    nueva_poblacion.append(cruzado)
                else:
                    nueva_poblacion.append(individuo)
            else:
                if pen_cruzado < pen_individuo:
                    nueva_poblacion.append(cruzado)
                else:
                    nueva_poblacion.append(individuo)
                    
        self.individuos = nueva_poblacion


def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = Poblacion(NP)  # Generar población aleatoria
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    mejor_es_factible = False
    
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F)  # Seleccionar, Mutar y Cruzar
        evaluaciones = poblacion.evaluar_poblacion()
        for idx, (eval, pen) in enumerate(evaluaciones):
            if pen == 0 and eval < mejor_evaluacion:
                mejor_individuo = poblacion.individuos[idx]
                mejor_evaluacion = eval
                mejor_es_factible = True
            elif pen > 0 and not mejor_es_factible:
                if eval < mejor_evaluacion:
                    mejor_individuo = poblacion.individuos[idx]
                    mejor_evaluacion = eval
                    mejor_es_factible = False

    return mejor_evaluacion, mejor_es_factible

def main():
    NP = 10
    CR = 0.9
    F = 0.9
    max_gen = 1000

    for i in range(25):
        mejor_evaluacion, es_factible = algoritmo_evolutivo(NP, CR, F, max_gen)
        final_fit.append((mejor_evaluacion, es_factible))
        
    return final_fit

if __name__ == '__main__':
    fitness = main()
    print(fitness)