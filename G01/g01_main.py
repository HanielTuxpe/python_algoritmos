import g01_Bounds as bound
import g01_Reflex as reflex
import time

class Comparacion:
    
    def excecute(self):

        print("Ejecutando Experimento Bounds")
        for _ in range(10):  
            print(".", end="", flush=True)
            time.sleep(0.5) 
        g01_Bound_Result = bound.main()
        for resultado in g01_Bound_Result:
            print(resultado)
        print("Experimento completado.\n")


        print("Ejecutando Experimento Reflex")
        for _ in range(10):  
            print(".", end="", flush=True)
            time.sleep(0.5) 
        g01_Reflex_Result =  reflex.main()
        for resultado in g01_Reflex_Result:
            print(resultado)
        print("Experimento completado.\n")

if __name__ == "__main__":
    graficador = Comparacion()
    graficador.excecute()
