class Aluno:
    def __init__(self, nome, idade, curso):
        self.nome = nome
        self.idade = idade
        self.curso = curso
        self.notas = []
    
    def apresentar(self):
        print(f"Olá, meu nome é {self.nome}, tenho {self.idade} anos e faço o curso de {self.curso}.")
    
    def calcular_media(self):
        total = 0
        if not self.notas:
            for nota in self.notas:
                total += nota
        else:
            print("O aluno não tem notas ainda")
        
        return total
