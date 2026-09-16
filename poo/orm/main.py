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
        return f"ID: {self.id}, Nome: {self.name}, Número: {self.contact}, Data: {self.date}"

db.connect()
db.create_tables([User])

while True:
    print("===== AGENDA DE CONTATOS =====")
    print("1. Cadastrar contato")
    print("2. Ver todos os contatos")
    print("3. Buscar contato pelo nome")
    print("4. Editar contato pelo ID")
    print("5. Excluir contato pelo ID")
    print("6. Drop table em tudo")
    print("7. Sair")

    choice = int(input("Escolha uma opção: "))

    match choice:
        case 1:
            name = input("Digite o nome do contato: ")
            contact = input("Digite o contato: ")
            User.create(name=name, contact=contact, default=datetime.datetime.now)
            print(f"Contato {name} cadastrado com sucesso!")
        case 2:
            all = User.select()
            for user in all:
                print(user)
        case 3:
            name = input("Qual o nome do contato que deseja buscar: ")
            user = User.get_or_none(User.name == name)
            print(user)
        case 4:
            id = input("Qual o id do contato que deseja editar: ")
            user = User.get_or_none(User.id == id)
            if user:
                user.name = input("Digite o novo nome para o contato: ")
                user.contact = input("Digte o novo número para o contato: ")
                user.save()
        case 5:
            id = input("Qual o id do contato que deseja excluir: ")
            user = User.get_or_none(User.id == id)
            if user:
                User.delete_instance(user)
                print("Contato excluído com sucesso")
            else:
                print("Id não encontrado!")

        case 6:
            pasword = input("Digite a senha de adm para continuar")
            if pasword == "y":
                querry = User.delete()
                querry.execute()
            else:
                print("Senha incorreta")
        case 7:
            print("Saindo...")
            break