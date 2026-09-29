alunos = [""] * 5

alunos[0] = "Fulano de tal"
alunos[1] = "Ciclano"

for i in range(2, len(alunos)):
    alunos[i] = input("Nome do aluno: ")
i = 0
while i < len(alunos):
    print(f"Aluno {i + 1}: {alunos[i]}")
    i += 1

