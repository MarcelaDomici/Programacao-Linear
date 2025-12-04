from random import random, choice
from metodosbasicos import  gerar_matriz_restricao, avalia_escala

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

def gerar_populacao_inicial(tamanho_populacao):
    matriz_restricao = gerar_matriz_restricao("A", tamanho_populacao)
    
    populacao = [gerar_solucao_embaralhada(matriz_restricao) for _ in range(tamanho_populacao)]
    return populacao

# Rever depois
def aptidao(populacao):
    tp = len(populacao)  
    fit = [0.0] * tp    
    soma = 0.0

    for i in range(tp):
        desvio = float(avalia_escala(populacao[i]))

        fit[i] = 1.0 / (1.0 + desvio)
        soma += fit[i]

    for i in range(tp):
        fit[i] = fit[i] / soma

    return fit

def roleta(fit):
    ale = random()
    soma = fit[0]
    i = 0
    while ale > soma and i < len(fit) - 1:
        i += 1
        soma += fit[i]
    return i

def cruzamento(ind1, ind2):
    dias = len(ind1[0])
    corte = random.randint(1, dias - 1)

    d1 = []
    d2 = []
    for linha, outra in zip(ind1, ind2):
        nova_coluna = linha[:corte] + outra[corte:]
        d1.append(nova_coluna)

        nova_coluna2 = outra[:corte] + linha[corte:]
        d2.append(nova_coluna2)
        return d1, d2

#print(aptidao(gerar_populacao_inicial(5)))
