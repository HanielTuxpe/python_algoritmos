import numpy as np

final_fit = []

class Poblacion:
    def __init__(self, NP):
        self.NP = NP
        self.Dim = 20
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        self._violaciones_individuo = []

    def generar_individuo(self):
        # Genera un individuo con 20 dimensiones, con valores aleatorios dentro de rangos específicos.
        return np.random.uniform(low=0, high=10, size=self.Dim)

    def evaluar(self, individuo):
        # Evalúa la función objetivo de un individuo, incluyendo una penalización por violación de restricciones.
        sum_cos4 = np.sum(np.cos(individuo)**4)
        prod_cos2 = np.prod(np.cos(individuo)**2)
        sum_ix2 = np.sum([(i + 1) * individuo[i]**2 for i in range(len(individuo))])
        f_x = -abs((sum_cos4 - 2 * prod_cos2) / np.sqrt(sum_ix2))
        return f_x

    def g1(self, x):
        return 0.75 - np.prod(x) <= 0

    def g2(self, x):
        return np.sum(x) - 7.5 * self.Dim <= 0

    def calcular_violaciones(self, x):
        self._violaciones = 0
        if not self.g1(x):
            self._violaciones += 1
        if not self.g2(x):
            self._violaciones += 1
        self._violaciones_individuo.append(self._violaciones)
        return self._violaciones

    def evaluar_poblacion(self):
        evaluaciones = [(self.evaluar(individuo), self.calcular_violaciones(individuo)) for individuo in self.individuos]
        return evaluaciones

    def mutacion(self, individuo, CR, F):
        # Realiza la mutación de un individuo.
        r1, r2, r3 = np.random.choice(self.NP, 3, replace=False)
        jrand = np.random.randint(0, len(individuo))
        nuevo_individuo = np.copy(individuo)
        for j in range(len(individuo)):
            if np.random.rand() < CR or j == jrand:
                nuevo_individuo[j] = self.individuos[r1][j] + F * (self.individuos[r2][j] - self.individuos[r3][j])
                nuevo_individuo = np.clip(nuevo_individuo, 0, 10)
        return nuevo_individuo

    def cruz(self, individuo1, individuo2):
        # Realiza la cruz de dos individuos.
        hijo = (individuo1 + individuo2) / 2
        hijo = np.clip(hijo, 0, 10)
        return hijo

    def seleccion(self, CR, F):
        # Realiza la selección, mutación y cruce para crear una nueva población.
        nueva_poblacion = []
        evaluaciones = self.evaluar_poblacion()
        for i in range(self.NP):
            individuo = self.individuos[i]
            mutado = self.mutacion(individuo, CR, F)
            cruzado = self.cruz(individuo, mutado)
            eval_cruzado, pen_cruzado = self.evaluar(cruzado), self.calcular_violaciones(cruzado)
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
    
    for _ in range(max_generaciones):
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
        print(f"Vuelta: {i}")
    return final_fit

if __name__ == '__main__':
    print(main())
