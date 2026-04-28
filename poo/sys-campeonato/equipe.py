from jogador import Jogador

class Equipe:
    def __init__(self, nome, jogo):
        self.nome = nome
        self.jogo = jogo
        self.jogadors = []
    
    def add_jogador(self, jogador):
        self.jogadors.append(jogador)
        print(f"{jogador.nome} adicionado a equipe {self.nome} com sucesso!😊")

    def print_jogadors(self):
        if (not self.jogadors):
            print(f"A equipe {self.nome} não tem nenhum jogador ainda!🚨")
            return

        for i in range(len(self.jogadors)):
            print(f"{i + 1}. {self.jogadors[i]}")
    
    def __str__(self):
        return f"{self.nome} | Jogo: {self.jogo}"