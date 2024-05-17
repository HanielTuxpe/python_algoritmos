import numpy as np
import matplotlib.pyplot as plt

import Boundexp1 as exp1
import Randomexp1 as exp2
import Reflexexp1 as exp3
import BoundForm5 as exp4
import ReflexForm5 as exp5
import RandomForm5 as exp6

class GraficoCajasEsfera:
    
    def ejecutar(self):
        # Obtener resultados
        print("Experimento 1")
        resultadoExp1 = exp1.main() 
        print("Experimento 2")
        resultadoExp2 = exp2.main()
        print("Experimento 3")
        resultadoExp3 = exp3.main()
        print("Experimento 4")
        resultadoExp4 = exp4.main()
        print("Experimento 5")
        resultadoExp5 = exp5.main()
        print("Experimento 6")
        resultadoExp6 = exp6.main()

        # Crear dos figuras separadas
        fig1 = plt.figure(figsize=(10, 6))
        fig2 = plt.figure(figsize=(10, 6))

        # Añadir subgráficos a cada figura
        ax1 = fig1.add_subplot(111)
        ax2 = fig2.add_subplot(111)

        # Diagramas de caja para el Problema 1 (PSO)
        ax1.boxplot([resultadoExp3, resultadoExp2, resultadoExp1], 
            labels=['Reflexión 1', 'Random 1', 'Límite 1'])
        ax1.set_xlabel('Problema')
        ax1.set_ylabel('Fitness')
        ax1.set_title('Comparación de los Problemas - Diferencia de Potencia')

        # Diagramas de caja para el Problema 2 (Esfera)
        ax2.boxplot([resultadoExp5, resultadoExp6, resultadoExp4], 
            labels=['Reflexión 2', 'Random 2', 'Límite 2'])
        ax2.set_xlabel('Problema')
        ax2.set_ylabel('Fitness')
        ax2.set_title('Comparación de los Problemas - Esfera')

        # Mostrar las dos figuras
        plt.show()

if __name__ == "__main__":
    graficador = GraficoCajasEsfera()
    graficador.ejecutar()
