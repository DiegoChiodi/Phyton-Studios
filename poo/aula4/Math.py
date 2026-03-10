import math

def print_optinos():
    print("1 - raiz quadrada")
    print("2 - arredondar para baixo")
    print("3 - arredondar para cima")
    print("4 - pegar parte inteira")
    print("5 - elevar a x")
    print("6 - sair do programa")

while (True):
    
    num = input("Digite um número para modificalo")

    print_optinos()

    options = int(input("Escolha uma opção: "))

    match(options):
        case 1:
            print(math.sqrt(num))
        case 2:
            print(math.floor(num))
        case 3:
            print(math.ceil(num))
        case 4:
            print(num // 1)
        case 5:
            print(num ** 3)
        case 6:
            break