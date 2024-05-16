import numpy as np
import matplotlib.pyplot as plt

# Función para generar un individuo aleatorio
def generar_individuo():
    return np.random.uniform(low=-20, high=20, size=2)

# Función para generar una población inicial de tamaño NP
def generar_poblacion(NP):
    poblacion = np.array([generar_individuo() for _ in range(NP)])
    return poblacion

# Función para evaluar la función objetivo de un individuo
def evaluar_individuo(individuo):
    x1, x2 = individuo
    # Función de aptitud: f(x1, x2) = (x1^3 + x2^3 )/ 100
    return (x1**3 + x2**3) / 100

# Función para evaluar la función objetivo de toda la población
def evaluar_poblacion(poblacion):
    evaluaciones = np.array([evaluar_individuo(individuo) for individuo in poblacion])
    return evaluaciones

# Función para realizar la mutación de un individuo
def mutacion(individuo, CR, F, poblacion):
    r1, r2, r3 = np.random.choice(len(poblacion), 3, replace=False)
    jrand = np.random.randint(0, len(individuo))
    nueva_individuo = np.copy(individuo)
    for j in range(len(individuo)):
        if np.random.rand() < CR or j == jrand:
            nueva_individuo[j] = poblacion[r1][j] + F * (poblacion[r2][j] - poblacion[r3][j])
    return nueva_individuo

# Función para realizar la cruz de dos individuos
def cruz(individuo1, individuo2):
    hijo = (individuo1 + individuo2) / 2
    # Aplicar restricción para asegurarse de que los valores estén dentro del rango [-20, 20]
    hijo = np.clip(hijo, -20, 20)
    return hijo

# Función para realizar la selección de un individuo
def seleccion(poblacion, CR, F):
    nueva_poblacion = []
    evaluaciones = evaluar_poblacion(poblacion)
    for i in range(len(poblacion)):
        individuo = poblacion[i]
        mutado = mutacion(individuo, CR, F, poblacion)
        cruzado = cruz(individuo, mutado)
        if evaluar_individuo(cruzado) <= evaluaciones[i]:
            nueva_poblacion.append(cruzado)
        else:
            nueva_poblacion.append(individuo)
    return np.array(nueva_poblacion)

def algoritmo_evolutivo(NP, CR, F, max_generaciones):
    poblacion = generar_poblacion(NP)
    inicial = poblacion
    mejor_individuo = None
    mejor_evaluacion = float('inf')  # Inicializar con un valor muy alto para minimización
    puntos_ultima_generacion = []  # Para almacenar los puntos de todos los individuos en la última generación
    for i in range(max_generaciones):
        poblacion = seleccion(poblacion, CR, F)
        evaluaciones = evaluar_poblacion(poblacion)
        mejor_individuo_idx = np.argmin(evaluaciones)
        if evaluaciones[mejor_individuo_idx] < mejor_evaluacion:
            mejor_individuo = poblacion[mejor_individuo_idx]
            mejor_evaluacion = evaluaciones[mejor_individuo_idx]
        if i == max_generaciones-1:
            puntos_generacion = [(individuo[0], individuo[1]) for individuo in poblacion]  # Obtener puntos de la generación actual
            puntos_ultima_generacion.extend(puntos_generacion)
        print(f"Generación {i+1}:")
        print(poblacion)
        print(f"mejor individuo {mejor_individuo}")
    # Devolver los puntos de todos los individuos en la última generación
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
plt.scatter(x_poblacion, y_poblacion, label='Población', alpha=0.3)
plt.scatter(x_ultima_generacion, y_ultima_generacion, color='red', label='Individuos Última Generación')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Puntos de la Población y Individuos de la Última Generación')
plt.legend()
plt.grid(True)
plt.show()