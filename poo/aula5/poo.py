class Campus:
    def __init__(self):
        self.name = ""
        self.cidade = ""
    
    def __str__(self):
        return f"Campus: {self.name}"

class Estudante:
    def __init__(self):
        self.data_nasc = ""
        self.cpf = ""
        self.name = ""
    
    def __str__(self):
        return f"Estudante: {self.name}"

class Curso:
    def __init__(self):
        self.name = ""
        self.duracao = 0
        self.periodo = 0
        self.campus = Campus()
    
    def __str__(self):
        return f"Curso: {self.name}"

class Matricula:
    def __init__(self):
        self.estudante = Estudante()
    def __str__(self):
        return f"Estudante: {self.estudante}"

diego = Estudante()
viado_do_kauan_que_ta_jogando = Estudante()
viado_do_regiani_que_ta_jogando = Estudante()

viado_do_kauan_que_ta_jogando.name = "Aaaaaaaa"
viado_do_regiani_que_ta_jogando.name = "Bbbbbbbb"

diego.name = "Diego"

print(diego)
print(viado_do_kauan_que_ta_jogando)
print(viado_do_regiani_que_ta_jogando)