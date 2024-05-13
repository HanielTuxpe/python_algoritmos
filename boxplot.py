import matplotlib.pyplot as plt
import numpy as np

# Generar datos aleatorios para los algoritmos 1 y 2
data_algoritmo1 = np.random.normal(loc=0, scale=1, size=100)
data_algoritmo2 = np.random.normal(loc=1, scale=1, size=100)  # Cambia loc para el algoritmo 2

print(data_algoritmo1, data_algoritmo2)

# Calcular el promedio de los datos para los algoritmos 1 y 2
promedio_algoritmo1 = np.mean(data_algoritmo1)
promedio_algoritmo2 = np.mean(data_algoritmo2)

# Crear el gráfico de caja y bigotes para el algoritmo 1
plt.boxplot(data_algoritmo1, positions=[1], widths=0.6, patch_artist=True)

# Crear el gráfico de caja y bigotes para el algoritmo 2
plt.boxplot(data_algoritmo2, positions=[2], widths=0.6, patch_artist=True)

# Añadir líneas horizontales para los promedios
plt.axhline(y=promedio_algoritmo1, color='r', linestyle='-', label=f'Promedio Algoritmo 1: {promedio_algoritmo1:.2f}')
plt.axhline(y=promedio_algoritmo2, color='b', linestyle='-', label=f'Promedio Algoritmo 2: {promedio_algoritmo2:.2f}')

# Ajustar posición de las etiquetas en el eje x
plt.xticks([1, 2], ['Algoritmo 1', 'Algoritmo 2'])

# Añadir título y etiquetas
plt.title('Comparación de Algoritmos')
plt.ylabel('Valores')

# Añadir leyenda
plt.legend()

# Mostrar el gráfico
plt.show()
