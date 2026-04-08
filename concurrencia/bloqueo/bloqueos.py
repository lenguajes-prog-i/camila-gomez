import threading 

contador = 0 
lock = threading.Lock()

def incrementador():
    global contador
    for _ in range (10000):
     with lock:
        contador += 1

hilo1 = threading.Thread(target=incrementador, args=())
hilo1.start()
hilo2 = threading.Thread(target=incrementador, args=())
hilo2.start()

hilo1.join()
hilo2.join()

print(contador)