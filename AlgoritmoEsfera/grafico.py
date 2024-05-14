import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Poblacion:
    
    def __init__(self, NP):
        self.NP = NP
        self.individuos = [self.generar_individuo() for _ in range(NP)]
        
    # Función para generar un individuo aleatorio
    def generar_individuo(self):
        return np.random.uniform(low=-80, high=80, size=2)  # Solo se generan 2 dimensiones

    # Función para evaluar la función objetivo de un individuo
    def evaluar(self, individuo):
        return individuo[0]**2 + individuo[1]**2  # Función de evaluación (ejemplo)

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

    # Función para aplicar restricción por reflexión
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
            if self.evaluar(cruzado) <= evaluaciones[i]:
                nueva_poblacion.append(cruzado)
            else:
                nueva_poblacion.append(individuo)
        self.individuos = nueva_poblacion

def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = Poblacion(NP)
    mejor_individuo = None
    mejor_evaluacion = float('inf')
    historial_evaluaciones = []  # Lista para almacenar las evaluaciones en cada generación
    for i in range(max_generaciones):
        poblacion.seleccion(CR, F)
        evaluaciones = poblacion.evaluar_poblacion()
        mejor_individuo_idx = np.argmin(evaluaciones)
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion.individuos[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        historial_evaluaciones.append(mejor_evaluacion)  # Guardar la mejor evaluación de la generación actual
    return mejor_individuo, mejor_evaluacion, historial_evaluaciones

# Llamar al algoritmo evolutivo para encontrar la mejor solución
NP = 10
CR = 0.9
F = 0.9
max_generaciones = 30
mejor_individuo, mejor_evaluacion, historial_evaluaciones = algoritmo_evolutivo(NP, CR, F, max_generaciones)

# Imprimir el mejor individuo y su mejor evaluación
print("Mejor individuo:", mejor_individuo)
print("Mejor evaluación:", mejor_evaluacion)

# Crear una malla de valores para x e y
x = np.linspace(-100, 100, 400)
y = np.linspace(-100, 100, 400)
X, Y = np.meshgrid(x, y)

# Evaluar la función en cada punto de la malla
Z = X**2 + Y**2

# Crear el gráfico tridimensional
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

# Mostrar la mejor solución encontrada por el algoritmo evolutivo en la gráfica
ax.scatter(mejor_individuo[0], mejor_individuo[1], mejor_evaluacion, color='red', s=100, label='Mejor Solución')

# Personalizar el gráfico
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Superficie tridimensional con la Mejor Solución')
ax.legend()

# Mostrar el gráfico
plt.show()
