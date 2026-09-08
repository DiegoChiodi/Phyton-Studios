from peewee import *
import datetime

db = SqliteDatabase('ranking.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField()
    contact = CharField()
    date = DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"Nome: {self.name}, Contato: {self.contact}, Data: {self.date}"


while True:
    print("===== AGENDA DE CONTATOS =====")
    print("1. Cadastrar contato")
    print("2. Ver todos os contatos")
    print("3. Buscar contato pelo nome")
    print("4. Editar contato pelo ID")
    print("5. Excluir contato pelo ID")
    print("6. Sair")

    choice = int(input("Escolha uma opção: "))

    match choice:
        case 1:
            name = input("Digite o nome do contato: ")
            contact = input("Digite o contato: ")
            user = User.create(
                name=name,
                contact=contact
            )
            print(f"Contato {user.name} cadastrado com sucesso!")
        case 2:
            all = User.select()
            for user in all:
                print(user)
        case 6:
            print("Saindo...")
            break

db.connect()
db.create_tables([User])