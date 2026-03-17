x = int(input("Digite o tamanho do vetor: "))

vetor = [[0] * 2 for _ in range(x)]
for i in range(x):
    for j in range(2):
        vetor[i][j] = int(input(f"Digite o valor do elemento no indíce {i}: "))

vetor.sort(key=lambda linha: linha[1])

cont = 0
ultimo_fim = 0
for inicio, fim in range(x):
    if inicio > ultimo_fim:
        cont += 1
        ultimo_fim = fim

print(cont)