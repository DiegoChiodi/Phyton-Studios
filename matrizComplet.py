def atribuirValoresParaMatriz(matriz):
    linhas = len(matriz)
    colunas = len(matriz[0])
    for i in range(linhas):
        for j in range(colunas):
            print(f"Digite o elemento [{i + 1}] [{j + 1}]")
            matriz[i][j] = int(input(''))
    return matriz
        
def somarMatriz(matrizA, matrizB):
    linhas = len(matrizA)
    colunas = len(matrizA[0])
    matriz = [[0] * colunas for _ in range(linhas)]
    for i in range(linhas):
        for j in range(colunas):
            matriz[i][j] = matrizA[i][j] + matrizB[i][j]

    return matriz

def subtrairMatriz(matrizA, matrizB):
    linhas = len(matrizA)
    colunas = len(matrizA[0])
    matriz = [[0] * colunas for _ in range(linhas)]

    for i in range(linhas):
        for j in range(colunas):
            matriz[i][j] = matrizA[i][j] - matrizB[i][j]

    return matriz


linhasA = int(input("informe a quantidade o linhas da matriz A: "))

colunasA = int(input("informe a quantidade de colunas da matriz A: "))

linhasB = int(input("informe a quantidade o linhas da matriz B: "))

colunasB  = int(input("informe a quantidade de colunas da matriz B: "))

if linhasA != linhasB or colunasA != colunasB:
    print("Erro")
else:
    matrizA = [[0] * colunasA for _ in range(linhasA)]
    matrizB = [[0] * colunasB for _ in range(linhasB)]

    print("preenchendo matriz A: ")
    matrizA = atribuirValoresParaMatriz(matrizA)

    print("preenchendo matriz B: ")
    matrizB = atribuirValoresParaMatriz(matrizB)

    print("A -> ", matrizA)
    print("B -> ", matrizB)

    matrizSoma = somarMatriz(matrizA, matrizB)
    print("Soma --> ", matrizSoma)
    matrizSubtrair = subtrairMatriz(matrizA, matrizB)
    print("Subtrair --> ", matrizSubtrair)
    