import pickle

def crear_auto(modelo, placa):
    return {"modelo": modelo, "placa": placa}
 
def representar_auto(auto):
    return f"El auto {auto['modelo']} tiene placa {auto['placa']}"

autos = [

crear_auto("BMW", "ABC123"),

crear_auto("Mercedes", "ACM123"),

crear_auto("Ferrari", "FLB123"),

crear_auto ("Toyota", "SLM121"),

crear_auto("Lamborghini", "JEA987")

]

with open("autos.txt", "wb") as archivo:
    pickle.dump(autos, archivo)

#Leer archivo

with open("autos.txt", "rb") as archivo:
    autos_cargados = pickle.load(archivo)


list(map(lambda auto: print(representar_auto(auto)), autos_cargados))
