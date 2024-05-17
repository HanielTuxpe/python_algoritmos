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
        resultadoExp1 = exp1.main() 
        resultadoExp2 = exp2.main()
        resultadoExp3 = exp3.main()
        resultadoExp4 = exp4.main()
        resultadoExp5 = exp5.main()
        resultadoExp6 = exp6.main()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Diagramas de caja para el Problema 1 (PSO)
        ax1.boxplot([resultadoExp3, resultadoExp2, resultadoExp1], 
            labels=['Reflexión 1', 'Restricción (Aleatorio) 1', 'Límite 1'])
        ax1.set_xlabel('Problema')
        ax1.set_ylabel('Fitness')
        ax1.set_title('Comparación de los Problemas - Diferencia de Potencia')

        # Diagramas de caja para el Problema 2 (Esfera)
        ax2.boxplot([resultadoExp5, resultadoExp6, resultadoExp4], 
            labels=['Reflexión 2', 'Restricción (Aleatorio) 2', 'Límite 2'])
        ax2.set_xlabel('Problema')
        ax2.set_ylabel('Fitness')
        ax2.set_title('Comparación de los Problemas - Esfera')

        # Mostrar el gráfico
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    graficador = GraficoCajasEsfera()
    graficador.ejecutar()
