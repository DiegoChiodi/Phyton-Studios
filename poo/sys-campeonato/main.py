from equipe import Equipe
from jogador import Jogador

equipes = []
jogadores = []

def cad_jogador():
    jogador = Jogador(input("Nome: "), input("turma: "), input("Nickname: "))
    jogadores.append(jogador)
    print("Jogador cadastrado com sucesso! 😊")

def cad_equipe():
    equipe = Equipe(input("Nome: "), input("Jogo: "))
    equipes.append(equipe)
    print("Equipe cadastrado com sucesso! 😊")

def add_jog_in_equipe():
    if (not jogadores):
        print(f"Não há nenhum jogador cadastrado ainda!🚨")
        return
    
    if (not equipes):
        print(f"Não há nenhuma equipe cadastrada ainda!🚨")
        return

    for i in range(len(jogadores)):
        print(f"{i + 1}. {jogadores[i]}")
    
    choosen_jog = int(input("Escolha o número de um jogador: "))

    for i in range(len(equipes)):
        print(f"{i + 1}. {equipes[i]}")
    
    choosen_equ = int(input("Escolha o número de uma equipe: "))
    
    if ((0 < choosen_equ and choosen_equ - 1 < len(equipes)) and (0 < choosen_jog and choosen_jog - 1 < len(jogadores))):
        if (equipes[choosen_equ] < 6):
            equipes[choosen_equ - 1].add_jogador(jogadores[choosen_jog - 1])
        else:
            print("A equipe já atingiu o limite de jogadores cadastrados! 🚨")
    else:
        print("Foi selecionado um número inválido")

def list_equ():
    if (not equipes):
        print(f"Nenhuma equipe foi cadastrada ainda!🚨")
        return

    for i in range(len(equipes)):
        print(f"{i + 1}. {equipes[i]}")

def list_jog():
    if (not jogadores):
        print(f"Nenhum jogador foi cadastrada ainda!🚨")
        return

    for i in range(len(jogadores)):
        print(f"{i + 1}. {jogadores[i]}")

def buscar_jog():
    nome = input("Digite o nome do jogador: ")

    for i in jogadores:
        if i.nome == nome:
            print(i)
            break

def rem_jog():
    for i in range(len(jogadores)):
        print(f"{i + 1}. {jogadores[i]}")
    
    choosen_jog = int(input("Escolha o número de um jogador para excluir: "))

    for i in len(equipes):
        for j in len(equipes[i]):
            if equipes[i][j] == choosen_jog:
                equipes[i].pop[j]
def run():
    opcao = 8
    try:
        while(opcao != 0):
            

            match (opcao):
                case 1:
                    cad_jogador()
                case 2:
                    cad_equipe()
                case 3:
                    add_jog_in_equipe()
                case 4:
                    list_equ()
                case 5:
                    list_jog()
                case 6:
                    buscar_jog()
                case 7:
                    rem_jog()
                case 8:
                    print("========================================")
                    print("  CAMPEONATO INTERCLASSE DE E-SPORTS")
                    print("========================================")
                    print("1. Cadastrar jogador")
                    print("2. Cadastrar equipe")
                    print("3. Adicionar jogador a uma equipe")
                    print("4. Listar todas as equipes")
                    print("5. Listar jogadores de uma equipe")
                    print("6. Buscar jogador por nickname")
                    print("7. Remover jogador")
                    print("8. Exibir opções do programa")
                    print("0. Sair")
                    print("========================================")
                case 0:
                    break
    
            opcao = int(input("Escolha uma opção: "))
    
    except Exception as erro:
        print("Ocorreu o erro:", erro)
        run()

run()

print("Obrigado por usar o programa!")