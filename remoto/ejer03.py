import pickle


class Auto:
    def __init__(self, modelo, placa):
        self.modelo = modelo
        self.placa = placa

    def __repr__(self):
        return f"El auto {self.modelo} tiene placa {self.placa}"


objeto_auto1 = Auto("Mazda", "ABC123")
objeto_auto2 = Auto("Mercedes1", "ABC153")
objeto_auto3 = Auto("Ferrari2", "ABC113")
objeto_auto4 = Auto("Lamborghini3", "ABC143")
objeto_auto5 = Auto("Toyota4", "ABC124")

mis_autos= [ objeto_auto1, objeto_auto2, objeto_auto3, objeto_auto4, objeto_auto5]

for miauto in mis_autos:
   archivo_auto = open("autos.txt", "wb")
   pickle.dump(objeto_auto1, archivo_auto)
   archivo_auto.close()


# Lectura en autos.txt
archivo_auto = open("autos.txt", "rb")
autos = pickle.load(archivo_auto)
archivo_auto.close()

print(autos)


