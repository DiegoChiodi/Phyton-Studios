nome = input("Nome: ")
idade = input("Idade: ")
salario = float(input("Salário: "))

print("Olá", nome, ". Você tem", idade, "anos.")
print(f"Olá {nome}. Você tem {idade}, anos.")

if (salario <= 10000):
    print(f"Você ganha muito mal. R${salario:.2f}")
else:
    print(f"Você ganha muito bem. R${salario:.2f}")