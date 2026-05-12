from animal import *

gato_1 = Gato("Tom", "gato", 4, "Desconhecido")

print(f"Meu gato é o {gato_1.nome}")
gato_1.respirar()
gato_1.ronronar()

cachorro = Cachorrro("Jake", "Cachorro", 4)

cachorro.respirar()
cachorro.abanar_rabo()

gato_1.rugir()
cachorro.rugir()