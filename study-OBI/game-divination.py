import random

sort_num = random.randint(1,100)

choice = 0
choices_cont = 0
while (choice != sort_num):
    choices_cont += 1
    if choices_cont > 1:
        choice = int(input('Digite outro valor: '))
    else:
       choice = int(input('Digite um valor de 1 a 100: '))
    if (choice > sort_num):
        print('O número sorteado é menor')
    elif (choice < sort_num):
        print('O número sorteado é maior')
    else:
        print('Parabéns você acertou em', choices_cont, 'tentativas!!!')
    