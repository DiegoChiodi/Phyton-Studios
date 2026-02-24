vetor_size = int(input('Digite o tamanho do vetor: '))

vetor = [0] * vetor_size

for i in range(vetor_size):
    vetor[i] = int(input("Digite um valor: "))

seq_max = 0
seq_temp = 0
for i in range(vetor_size):
    if vetor[i - 1] < vetor[i]:
        seq_temp += 1
    else:
        if seq_max < seq_temp:
            seq_max = seq_temp
        seq_temp = 0
    

if seq_max < seq_temp:
    seq_max = seq_temp
print(seq_max)