import numpy as np

final_fit = []

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    def generar_individuo(self):
        # Genera un individuo con 13 dimensiones, con valores aleatorios dentro de rangos específicos según la formula.
        individuo = np.zeros(13)
        individuo[:4] = np.random.uniform(low=0, high=1, size=4)
        individuo[4:9] = np.random.uniform(low=0, high=1, size=5)
        individuo[9:12] = np.random.uniform(low=0, high=10, size=3)
        individuo[12] = np.random.uniform(low=0, high=1)
        return individuo

    def evaluar(self, individuo):
        # Evalúa la función objetivo de un individuo, incluyendo una penalización por violación de restricciones.
        x = individuo
        fitness = 5 * np.sum(x[:4]) - 5 * np.sum(x[:4]**2) - np.sum(x[4:])
        restricciones = self.evaluar_restricciones(individuo)
        penalizacion = sum([max(0, r) for r in restricciones])
        fitness += penalizacion * 10000
        return fitness, penalizacion

    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar(individuo) for individuo in self.individuos]
        return evaluaciones

    def evaluar_restricciones(self, individuo):
        x = individuo
        #Restricciones propuestas por la fórmula G01
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

    def cumple_restricciones(self, individuo):
        # Verifica si un individuo cumple con todas las restricciones.
        restricciones = self.evaluar_restricciones(individuo)
        return all(r <= 0 for r in restricciones)

    def mutacion(self, individuo, CR, F):
        # Realiza la mutación de un individuo.
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
                
                # Refleja los valores que están fuera de los límites
                if j < 9:
                    nuevo_individuo[j] = min(max(nuevo_individuo[j], 0), 1)
                elif j < 12:
                    nuevo_individuo[j] = min(max(nuevo_individuo[j], 0), 100)
                else:
                    nuevo_individuo[j] = min(max(nuevo_individuo[j], 0), 1)
        return nuevo_individuo

    def cruz(self, individuo1, individuo2):
        # Realiza la cruz de dos individuos.
        hijo = (individuo1 + individuo2) / 2
        # Refleja los valores que están fuera de los límites
        hijo[:9] = np.minimum(np.maximum(hijo[:9], 0), 1)
        hijo[9:12] = np.minimum(np.maximum(hijo[9:12], 0), 100)
        hijo[12] = np.minimum(np.maximum(hijo[12], 0), 1)
        return hijo

    def seleccion(self, CR, F):
        # Realiza la selección, mutación y cruce para crear una nueva población.
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            eval_cruzado, pen_cruzado = self.evaluar(cruzado)
            eval_individuo, pen_individuo = evaluaciones[i]
            
            # Siempre prefiere soluciones factibles
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
    # Ejecuta el algoritmo evolutivo.
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
    # Ejecuta el algoritmo evolutivo múltiples veces y guarda los mejores resultados.
    NP = 100
    CR = 0.9
    F = 0.9
    max_gen = 1000

    for i in range(25):
        mejor_evaluacion, es_factible = algoritmo_evolutivo(NP, CR, F, max_gen)
        final_fit.append((mejor_evaluacion, es_factible))
        
    return final_fit

if __name__ == '__main__':
    fitness = main()
