import threading
import time

def tarea(letra):
    
    print(f'Hilo de la letra: {letra * 5}')

hilos = []
inicio = time.perf_counter()

for i in range(65, 78):
    letra = chr(i)
    hilo = threading.Thread(target=tarea, args=(letra,))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

fin = time.perf_counter()

tiempo_total = fin - inicio
print(f"Tiempo total de ejecución: {tiempo_total:} segundos")