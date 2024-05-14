import numpy as np

def sphere_function(x):
    """
    Función de esfera en 10 dimensiones.
    
    Args:
    x (numpy array): Vector de entrada de 10 dimensiones.
    
    Returns:
    float: Valor de la función de esfera evaluada en x.
    """
    return np.sum(x**2)

def evolucion_diferencial(f, limites, NP, F, CR, max_iter):
    """
    Evolución diferencial para encontrar el mínimo de una función.
    
    Args:
    f (function): Función objetivo a minimizar.
    limites (numpy array): Límites de las variables.
    NP (int): Tamaño de la población.
    F (float): Factor de escala.
    CR (float): Tasa de recombinación cruzada.
    max_iter (int): Número máximo de iteraciones.
    
    Returns:
    numpy array: Mejor solución encontrada.
    """
    D = len(limites)
    X = np.random.rand(NP, D) * (limites[:, 1] - limites[:, 0]) + limites[:, 0]
    g = 0
    while g < max_iter:
        for i in range(NP):
            r1, r2, r3 = np.random.choice(NP, 3, replace=False)
            jrand = np.random.randint(0, D)
            trial_vector = np.copy(X[i])
            for j in range(D):
                randj = np.random.rand()
                if randj < CR or j == jrand:
                    trial_vector[j] = X[r1, j] + F * (X[r2, j] - X[r3, j])
            trial_vector = manejar_restricciones(trial_vector, limites)
            if f(trial_vector) < f(X[i]):
                X[i] = trial_vector
        g += 1
    return X

def manejar_restricciones(x, limites):
    """
    Manejo de restricciones para asegurar que los valores estén dentro de los límites.
    
    Args:
    x (numpy array): Vector de entrada.
    limites (numpy array): Límites de las variables.
    
    Returns:
    numpy array: Vector de entrada con restricciones aplicadas.
    """
    for i in range(len(x)):
        if x[i] < limites[i, 0]:
            x[i] = limites[i, 0]
        elif x[i] > limites[i, 1]:
            x[i] = limites[i, 1]
    return x

# Ejemplo de uso:
limites = np.array([[-5, 5]] * 10)  # Límites de las variables para 10 dimensiones
NP = 10  # Tamaño de la población
F = 0.5  # Factor de escala
CR = 0.9  # Tasa de recombinación cruzada
max_iter = 100  # Número máximo de iteraciones

# Llamada a la función de evolución diferencial
resultado = evolucion_diferencial(sphere_function, limites, NP, F, CR, max_iter)

# Impresión de resultados
print("Mejor solución encontrada:", resultado[0])
print("Valor de la función objetivo:", sphere_function(resultado[0]))
