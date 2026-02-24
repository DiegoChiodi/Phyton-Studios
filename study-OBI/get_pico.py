vetor_size = int(input('Digite o tamanho do vetore: '))

vetor = [0] * vetor_size


for i in range(vetor_size):
    vetor[i] = int(input('Digite um valor: '))

found_pico = False
ascend = 0
pico_is_valid = False
ascend_one = False
dascend_one = False

for i in range(1, vetor_size):
    if vetor[i-1] < vetor[i]:
        ascend = 1
    elif vetor[i-1] == vetor[i]:
        ascend = 0
    else:
        ascend = -1
    
    if ascend == 1:
        if found_pico:
            pico_is_valid = False
            break
        ascend_one = True
    elif ascend == 0:
        pico_is_valid = False
        break
    else:
        if found_pico:
            ascend_one = True
        elif ascend_one:
            found_pico = True
            pico_is_valid = True

print(pico_is_valid)