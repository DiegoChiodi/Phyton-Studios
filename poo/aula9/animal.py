class Animal:
    def __init__(self, nome, especie, patas):
        self.nome = nome
        self.especie = especie
        self.patas = patas
    
    def respirar(self):
        print("Respirando")
    
    def rugir(self):
        print("Rugir")

class Cachorrro(Animal):
    def abanar_rabo(self):
        print("Cachorro abanou rabo")
    
    def rugir(self):
        print("Au au")

class Gato(Animal):
    def ronronar(self):
        print("Gato ranronou")
        
    def rugir(self):
        print("Miau")