class Jogador:
    def __init__(self, nome, turma, nickname):
        self.nome = nome
        self.turma = turma
        self.nickname = nickname
    
    def __str__(self):
        return f"{self.nome} ({self.nickname}) - {self.turma}"