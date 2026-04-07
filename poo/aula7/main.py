from aluno import Aluno

aluno1 = Aluno(input("Digite o nome do aluno: "), int(input('Digite a idade do aluno: ')), input("Digite o curso do aluno: "))
print(aluno1.apresentar()) # Saída: Olá, meu nome é Lucas, tenho 16 anos e faço o curso de Informática.

for i in range(3):
    aluno1.notas.append(float(input(f"Digite a {i}º nota: ")))

print(f"A média do estudante é: {aluno1.calcular_media()}")