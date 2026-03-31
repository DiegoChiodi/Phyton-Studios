class Bank_Account:
    def __init__(self, num_cont, nom_tit, sal_disp):
        self.num_cont = num_cont
        self.nom_tit = nom_tit
        self.sal_disp = sal_disp
    
    def deposit(self, valor):
        self.sal_disp += valor
        print("Depósito realizado com sucesso!")
        print(f"Novo saldo de {self.nom_tit}: R${self.sal_disp}")
    
    def sacar(self, valor):
        if (self.sal_disp - valor >= 0):
            self.sal_disp -= valor
            print("Saque realizado com sucesso!")
            print(f"Novo saldo de {self.nom_tit}: R${self.sal_disp}")
        else:
            print("Saldo insuficiente para saque!")
            print(f"Saldo atual de {self.nom_tit}: R$ {self.sal_disp:.2f}")

    def transference(self, target, valor):
        if (self.sal_disp - valor >= 0 and valor >= 0):
            self.sal_disp -= valor
            target.sal_disp += valor
            print("Transferência realizada com sucesso!")
            print(f"Novo saldo de {self.nom_tit}: R${self.sal_disp}")
            print(f"Novo saldo de {target.nom_tit}: R${target.sal_disp}")
        else:
            print("Saldo insuficiente para transferência!")
            print(f"Saldo atual de {self.nom_tit}: R$ {self.sal_disp:.2f}")

    def __str__(self):
        return f"{self.nom_tit}: R${self.sal_disp}"


cont_1 = Bank_Account(input("Digite o número da conta: "), input("Digite o nome do titular: "), float(input("Digite o saldo disponível inicialmente: ")))
cont_2 = Bank_Account(input("Digite o número da conta: "), input("Digite o nome do titular: "), float(input("Digite o saldo disponível inicialmente: ")))
print("Saldo inicial:")
print(cont_1)
print(cont_2)

cont_1.deposit(float(input(f"Escolha o quanto deseja depositar na conta de {cont_1.nom_tit}: ")))

cont_2.sacar(float(input(f"Escolha o quanto deseja sacar da conta de {cont_2.nom_tit}: ")))

cont_1.transference(cont_2, float(input(f"Escolha o quanto {cont_1.nom_tit} vai transferir para {cont_2.nom_tit}: ")))

cont_2.sacar(float(input(f"Escolha o quanto deseja sacar da conta de {cont_2.nom_tit}: ")))

print(cont_1)
print(cont_2)