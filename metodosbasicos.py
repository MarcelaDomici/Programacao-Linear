from random import randint
from numpy import array, std

n_funcionarios = 5
N_DIAS = 30

# 5 funcionários, 30 dias
# Matriz usada na solução de tipo "FIXO"
MATRIZ_RESTRICAO_FIXA = [
    [1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def gerar_matriz_restricao(tipo, funcs=n_funcionarios, dias=N_DIAS):
    if tipo == "F":
        return array(MATRIZ_RESTRICAO_FIXA)
    else:
        while True:
            matriz = []
            for _ in range(funcs):   
                linha = []
                for _ in range(dias):
                    linha.append(randint(0,1)) 
                matriz.append(linha)  
            array_np = array(matriz)
            if dias_sem_funcionarios(array_np):
                return array_np

def dias_sem_funcionarios(matriz):
    for j in range(len(matriz[0])):

        if sum(matriz[:, j]) == 0:
            #print(f'Dia {j} sem funcionários, gerar novamente.')
            return False
    return True

# Para DEBUG
def imprime_matriz(matriz):
    print("Matriz: ")
    for linha in matriz:
        print(linha)

def gerar_solucao_inicial(matriz):
    funcs = len(matriz)
    dias = len(matriz[0])
    escala = []
    for _ in range(funcs):
        escala.append([0]*dias)

    for dia in range(dias):
        for func in range(funcs):
            if matriz[func][dia] == 1:
                escala[func][dia] = 1
                break
    return escala

# Calcula o desvio padrão do número de dias trabalhados por funcionário (menor, melhor)
def avalia_escala(escala):
    dias_trabalhados = []
    for func in escala:
        total = 0
        for dia in func:
            total += dia
        dias_trabalhados.append(total)

    desvio_padrao = std(dias_trabalhados)
    return desvio_padrao