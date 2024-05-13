import numpy as np
import matplotlib.pyplot as plt

# Definición de la función objetivo
def funcion_objetivo(x):
    return sum(x ** 2)

# Función para evolución diferencial
def evolucion_diferencial(f, limites, NP, F, CR, max_iter):
    D = len(limites)
    X = np.random.rand(NP, D) * (limites[:, 1] - limites[:, 0]) + limites[:, 0]
    g = 0
    while g < max_iter:
        for i in range(NP):
            r1, r2, r3 = np.random.choice(NP, 3, replace=False)
            jrand = np.random.randint(0, D)
            for j in range(D):
                randj = np.random.rand()
                if randj < CR or j == jrand:
                    X[i, j] = X[r1, j] + F * (X[r2, j] - X[r3, j])
                else:
                    X[i, j] = X[i, j]
            X[i] = manejar_restricciones(X[i], limites)
            if f(X[i]) <= f(X[i - 1]):
                X[i - 1] = X[i]
            else:
                X[i] = X[i - 1]
        g += 1
    return X

# Función para manejar restricciones
def manejar_restricciones(x, limites):
    for i in range(len(x)):
        if x[i] < limites[i, 0]:
            x[i] = limites[i, 0]
        elif x[i] > limites[i, 1]:
            x[i] = limites[i, 1]
    return x

# Parámetros
limites = np.array([[-20, 20]] * 2)
NP = 10
F = 0.9
CR = 0.9
max_iter = 30

# Ejecución del algoritmo
resultado = evolucion_diferencial(funcion_objetivo, limites, NP, F, CR, max_iter)

# Gráfico de los puntos generados
plt.scatter(resultado[:, 0], resultado[:, 1], c='r', marker='o', label='Puntos generados')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Puntos generados por el algoritmo de evolución diferencial')
plt.grid(True)
plt.legend()
plt.show()
