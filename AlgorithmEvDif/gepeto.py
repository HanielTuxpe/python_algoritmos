import numpy as np
import matplotlib.pyplot as plt

class Poblacion:
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]

    def generar_individuo(self):
        return np.random.uniform(low=-20, high=20, size=2)

    def evaluar(self, individuo):
        x1, x2 = individuo
        return (x1**3 + x2**3) / 100

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

    def cruz(self, individuo1, individuo2):
        hijo = (individuo1 + individuo2) / 2
        hijo = np.clip(hijo, -20, 20)
        return hijo

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
    poblacion = Poblacion(NP)
    inicial = poblacion.individuos
    mejor_individuo = None
    mejor_evaluacion = float('inf')  # Inicializar con un valor muy alto para minimización
    puntos_ultima_generacion = []  # Para almacenar los puntos de todos los individuos en la última generación
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F)
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        if i == max_generaciones - 1:
            puntos_generacion = [(individuo[0], individuo[1]) for individuo in poblacion.individuos]  # Obtener puntos de la generación actual
            puntos_ultima_generacion.extend(puntos_generacion)
        print(f"Generación {i+1}:")
        print(poblacion.individuos)
        print(f"mejor individuo {mejor_individuo}")
    # Devolver los puntos de todos los individuos en la última generación y la población inicial
    return puntos_ultima_generacion, inicial

# Ejemplo de uso
NP = 10
CR = 0.9
F = 0.9
max_generaciones = 30
puntos_ultima_generacion, inicial = algoritmo_evolutivo(NP, CR, F, max_generaciones)

# Extraer todos los puntos de la población
poblacion_puntos = [individuo.tolist() for individuo in inicial]
x_poblacion, y_poblacion = zip(*poblacion_puntos)

# Convertir puntos de la última generación a arrays separados de x e y
x_ultima_generacion, y_ultima_generacion = zip(*puntos_ultima_generacion)

# Graficar todos los puntos de la población y los individuos de la última generación
plt.scatter(x_poblacion, y_poblacion, label='Población Inicial', alpha=0.3)
plt.scatter(x_ultima_generacion, y_ultima_generacion, color='red', label='Individuos Última Generación')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Puntos de la Población y Individuos de la Última Generación')
plt.legend()
plt.grid(True)
plt.show()
