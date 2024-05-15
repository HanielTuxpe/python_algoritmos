import numpy as np
import random as rd
import math
import matplotlib.pyplot as plt

class EAGDE:
    MEJORES_SOLUCIONES = []

    # Definir parámetros
    NP = 30  # Tamaño de la población
    GMAX = 50  # Número máximo de generaciones
    DIM = 10  # Dimensión del vector de solución

    # Limites de generación para el individuo
    MAX = 100  # Máximo de valor en la población
    MIN = -100  # Mínimo de valor en la población

    # Limites de búsqueda
    O_MAX = 80
    O_MIN = -80

    F5 = -1000

    CR = 0.8
    F = 0.5

    def _init_(self):
        self._poblacion = np.zeros((self.NP, self.DIM))
        self._o = np.zeros(self.DIM)
        self.generar_poblacion()
        self._o = self.generar_o()

    def generar_individuo(self) -> np.ndarray:
        # Creando individuo
        _individuo = []
        # Repite el número de veces de la dimensión
        for _ in range(self.DIM):
            # Concatena a la lista del individuo un número aleatorio
            _individuo.append(rd.uniform(self.MIN, self.MAX))
        # Regresar un objeto np array
        return np.array(_individuo)

    def generar_o(self) -> np.ndarray:
        # Creando el vector "o"
        _o = []
        # Repite el número de veces de la dimensión
        for _ in range(self.DIM):
            # Concatena a la lista del vector "o" un número aleatorio
            _o.append(rd.uniform(self.O_MIN, self.O_MAX))
        # Regresar un objeto np array
        return np.array(_o)

    def generar_poblacion(self):
        # Generación de la población
        for i in range(self.NP):
            # Se obtiene el individuo
            individuo = self.generar_individuo()
            # Se añade a la población
            self._poblacion[i] = individuo

    def crossover(self, v1, v2, CR):
        mascara = np.random.rand(self.DIM) < CR
        cruzado = np.where(mascara, v1, v2)
        return cruzado

    def start(self):
        f = [self._function_power_different(_individuo) for _individuo in self._poblacion]

        best_index = f.index(min(f))
        best = self._poblacion[best_index]

        for g in range(1, self.GMAX + 1):
            _descendencia = []

            # Descendencia
            for i in range(self.NP):
                r1, r2 = rd.sample(range(self.NP), 2)
                while r1 == r2 or r2 == i:
                    r1, r2 = rd.sample(range(self.NP), 2)
                x1, x2 = self._poblacion[r1], self._poblacion[r2]

                v = np.zeros(self.DIM)

                for j in range(self.DIM):
                    if rd.random() < self.CR or j == rd.randint(0, self.DIM - 1):
                        v[j] = best[j] + self.F * (x1[j] - x2[j])
                    else:
                        v[j] = self._poblacion[i][j]

                v = self.apply_bounds(v)

                f_v = self._function_power_different(v)

                if f_v < f[i]:
                    _descendencia.append(v)
                else:
                    _descendencia.append(self._poblacion[i])

            self._poblacion = _descendencia

            f = [self._function_power_different(_individuo) for _individuo in self._poblacion]

            mejor_indice = f.index(min(f))
            mejor = self._poblacion[mejor_indice]

            self.MEJORES_SOLUCIONES.append(mejor)

        self._plot_convergence()

    def apply_bounds(self, vector):
        return np.clip(vector, self.MIN, self.MAX)

    def calcular_z(self, x):
        # Creo arreglo de z
        _arr_z = np.zeros((self.DIM))
        # Inicio iteración mediante la Dimensión
        for i in range(self.DIM):
            # Validación de los límites
            _arr_z[i] = self.restriccion(x[i] - self._o[i])
        # Devuelvo arreglo z
        return _arr_z

    def _function_power_different(self, x):
        suma = 0
        _arr_z = self.calcular_z(x)
        for j in range(self.DIM):
            z = _arr_z[j]
            e = abs(z) ** (2 + 4 * (j / (self.DIM - 1)))
            suma += e
        res = math.sqrt(suma) - self.F5
        return res

    def _plot_convergence(self):
        # Obtener el valor de la función para cada mejor solución por generación
        fitness_values = [self._function_power_different(solution) for solution in self.MEJORES_SOLUCIONES]

        # Ordenar los valores de fitness en orden descendente
        fitness_values_sorted = sorted(fitness_values, reverse=True)

        # Graficar
        plt.plot(range(1, self.GMAX + 1), fitness_values_sorted, marker='o', linestyle='-')
        plt.title('Convergencia del algoritmo EAGDE')
        plt.xlabel('Generación')
        plt.ylabel('Valor de la función')
        plt.grid(True)
        plt.yscale('log')  # Usar escala logarítmica si los valores son muy dispares
        plt.show()

    def restriccion(self, individuo):
        if individuo > self.MAX or individuo < self.MIN:
            individuo = self.MIN + rd.random() * (self.MAX - self.MIN)
        return individuo

    def _str_(self) -> str:
        return f"{self._poblacion}"


def main():
    eagde = EAGDE()
    print(eagde)
    eagde.start()


if _name_ == "_main_":
    main()