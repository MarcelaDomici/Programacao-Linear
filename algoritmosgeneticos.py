from random import shuffle, choice
from metodosbasicos import  gerar_matriz_restricao, gerar_solucao_inicial, imprime_matriz

def gerar_solucao_embaralhada(matriz_restricao):
    funcs = len(matriz_restricao)    
    dias = len(matriz_restricao[0])   
    novo_individuo = [[0]*dias for _ in range(funcs)]

    for dia in range(dias):
        restricoes_validas = []
        for f in range(funcs):
            if matriz_restricao[f][dia] == 1:
                restricoes_validas.append(f)

        if restricoes_validas:
            escolhido = choice(restricoes_validas)

            for f in range(funcs):
                novo_individuo[f][dia] = 0
            novo_individuo[escolhido][dia] = 1

    return novo_individuo

def gerar_populacao_inicial(tamanho_populacao: int):
    matriz_restricao = gerar_matriz_restricao("A", tamanho_populacao)
    
    populacao = [gerar_solucao_embaralhada(matriz_restricao) for _ in range(tamanho_populacao)]
    return populacao

# É pra gerar 5
# populacao_inicial = gerar_populacao_inicial(5)
# print(f"População inicial gerada com {len(populacao_inicial)} indivíduos.")
# imprime_matriz(populacao_inicial)