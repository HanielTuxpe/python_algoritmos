from Algoritmo_Genetico_1 import _main, _fitness
from Algoritmo_Genetico_2 import main, fitness
import numpy as np
import matplotlib.pyplot as plt


if __name__ == '__main__':
    for i in range(25):
        _main()
        main()

    _fitness_array = np.array(_fitness)
    fitness_array = np.array(fitness)

    print("################################")

    average_genetic_1 = float(np.average(_fitness_array))
    average_genetic_2 = float(np.average(fitness_array))

    print("################################")

    print(f"Promedio de algoritmo genetico 1: {average_genetic_1}")
    print(f"Promedio de algoritmo genetico 2: {average_genetic_2}")

    print(type(average_genetic_1))

        # Crear el gráfico de caja y bigotes para el algoritmo 1
    plt.boxplot(average_genetic_1, positions=[1], widths=0.6, patch_artist=True)

    # Crear el gráfico de caja y bigotes para el algoritmo 2
    plt.boxplot(average_genetic_2, positions=[2], widths=0.6, patch_artist=True)

    # Añadir líneas horizontales para los promedios
    plt.axhline(y=average_genetic_1, color='r', linestyle='-', label=f'Promedio Algoritmo 1: {average_genetic_1:.2f}')
    plt.axhline(y=average_genetic_2, color='b', linestyle='-', label=f'Promedio Algoritmo 2: {average_genetic_2:.2f}')

    # Ajustar posición de las etiquetas en el eje x
    plt.xticks([1, 2], ['Algoritmo 1', 'Algoritmo 2'])

    # Añadir título y etiquetas
    plt.title('Comparación de Algoritmos')
    plt.ylabel('Valores')

    # Añadir leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()



    
    


