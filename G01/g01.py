import numpy as np

final_fit = []

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    def generar_individuo(self):
        return np.random.uniform(low=-100, high=100, size=13)

    def evaluar(self, individuo):
        x = individuo
        fitness = 5 * np.sum(x[:4]) - 5 * np.sum(x[:4]**2) - np.sum(x[4:])
        return fitness

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

    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar(individuo) for individuo in self.individuos]
        return evaluaciones

    def cumple_restricciones(self, individuo):
        restricciones = self.evaluar_restricciones(individuo)
        e = all(r <= 0 for r in restricciones)
        return e

    def rest_reflex(self, valores, inf_lim, sup_lim):
        for i in range(len(valores)):
            if valores[i] < inf_lim[i]:
                valores[i] = 2 * inf_lim[i] - valores[i]
            elif valores[i] > sup_lim[i]:
                valores[i] = 2 * sup_lim[i] - valores[i]
        return valores

    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        nuevo_individuo = self.rest_reflex(nuevo_individuo, inf_lim, sup_lim)
        return nuevo_individuo

    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        hijo = self.rest_reflex(hijo, inf_lim, sup_lim)
        return hijo

    def aplicar_limites(self, individuo):
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        return self.rest_reflex(individuo, inf_lim, sup_lim)

    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            if self.evaluar(cruzado) <= evaluaciones[i] and self.cumple_restricciones(cruzado):
                nueva_poblacion.append((cruzado, True))
            else:
                nueva_poblacion.append((individuo, False))
        self.individuos = nueva_poblacion

def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = Poblacion(NP)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    mejor_es_factible = False
    violaciones = float('inf')
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F)
        for individuo, es_factible in poblacion.individuos:
            fitness = poblacion.evaluar(individuo)
            if fitness < mejor_evaluacion:
                if es_factible:
                    mejor_individuo = individuo
                    mejor_evaluacion = fitness
                    mejor_es_factible = True
                else:
                    violaciones_actual = sum(1 for r in poblacion.evaluar_restricciones(individuo) if r > 0)
                    if violaciones_actual < violaciones:
                        mejor_individuo = individuo
                        mejor_evaluacion = fitness
                        mejor_es_factible = False
                        violaciones = violaciones_actual
    return mejor_evaluacion, mejor_es_factible

def main():
    NP = 13
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
import numpy as np

final_fit = []

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    def generar_individuo(self):
        return np.random.uniform(low=-100, high=100, size=13)

    def evaluar(self, individuo):
        x = individuo
        fitness = 5 * np.sum(x[:4]) - 5 * np.sum(x[:4]**2) - np.sum(x[4:])
        return fitness

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

    def evaluar_poblacion(self):
        evaluaciones = [self.evaluar(individuo) for individuo in self.individuos]
        return evaluaciones

    def cumple_restricciones(self, individuo):
        restricciones = self.evaluar_restricciones(individuo)
        e = all(r <= 0 for r in restricciones)
        return e

    def rest_reflex(self, valores, inf_lim, sup_lim):
        for i in range(len(valores)):
            if valores[i] < inf_lim[i]:
                valores[i] = 2 * inf_lim[i] - valores[i]
            elif valores[i] > sup_lim[i]:
                valores[i] = 2 * sup_lim[i] - valores[i]
        return valores

    def mutacion(self, individuo, CR, F):
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        nuevo_individuo = self.rest_reflex(nuevo_individuo, inf_lim, sup_lim)
        return nuevo_individuo

    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        hijo = self.rest_reflex(hijo, inf_lim, sup_lim)
        return hijo

    def aplicar_limites(self, individuo):
        inf_lim = np.array([0]*9 + [0]*3 + [0])
        sup_lim = np.array([1]*9 + [100]*3 + [1])
        return self.rest_reflex(individuo, inf_lim, sup_lim)

    def seleccion(self, CR, F):
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            if self.evaluar(cruzado) <= evaluaciones[i] and self.cumple_restricciones(cruzado):
                nueva_poblacion.append((cruzado, True))
            else:
                nueva_poblacion.append((individuo, False))
        self.individuos = nueva_poblacion

def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = Poblacion(NP)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    mejor_es_factible = False
    violaciones = float('inf')
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F)
        for individuo, es_factible in poblacion.individuos:
            fitness = poblacion.evaluar(individuo)
            if fitness < mejor_evaluacion:
                if es_factible:
                    mejor_individuo = individuo
                    mejor_evaluacion = fitness
                    mejor_es_factible = True
                else:
                    violaciones_actual = sum(1 for r in poblacion.evaluar_restricciones(individuo) if r > 0)
                    if violaciones_actual < violaciones:
                        mejor_individuo = individuo
                        mejor_evaluacion = fitness
                        mejor_es_factible = False
                        violaciones = violaciones_actual
    return mejor_evaluacion, mejor_es_factible

def main():
    NP = 13
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
