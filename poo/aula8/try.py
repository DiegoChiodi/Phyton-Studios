try:
    idade = int(input("idade: "))
    idade_nova = idade + 5
    print("Sua idade daqui 5 anos será", idade_nova)
except Exception as error:
    idade = 0
    print("Idade inválida!!")
    print(str(error))

