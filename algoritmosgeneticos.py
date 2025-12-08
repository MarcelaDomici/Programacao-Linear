from random import random, choice, randint
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

def gerar_populacao_inicial(tamanho_populacao, matriz_restricao):
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
    funcs = len(ind1)
    dias = len(ind1[0])
    corte = randint(1, dias - 1)

    d1 = [[0]*dias for _ in range(funcs)]
    d2 = [[0]*dias for _ in range(funcs)]

    for dia in range(corte):
        for f in range(funcs):
            d1[f][dia] = ind1[f][dia]
            d2[f][dia] = ind2[f][dia]

    for dia in range(corte, dias):
        for f in range(funcs):
            d1[f][dia] = ind2[f][dia]
            d2[f][dia] = ind1[f][dia]

    return d1, d2


def mutacao(individuo, matriz_restricao):
    funcs = len(individuo)
    dias = len(individuo[0])
    d = randint(0, dias - 1)

    validos = [f for f in range(funcs) if matriz_restricao[f][d] == 1]

    if not validos:
        print('Erro: matriz de restrição não respeitada')
        print(validos)
        print(individuo)
        print(d)
        print(matriz_restricao)
        return individuo

    escolhido = choice(validos)

    for f in range(funcs):
        individuo[f][d] = 0
    individuo[escolhido][d] = 1

    return individuo


def descendente(n, pop, fit, tp, tc, tm, matriz_restricao):
    qc = tp
    qd = 2 * qc
    descendentes = []

    for i in range(0, qd, 2):
        p1 = roleta(fit)
        p2 = roleta(fit)

        ale = random()
        if ale < tc:
            d1, d2 = cruzamento(pop[p1], pop[p2])
        else:
            d1, d2 = pop[p1], pop[p1]

        ale = random()
        if ale < tm:
            d1 = mutacao(d1, matriz_restricao)

        ale = random()
        if ale < tm:
            d2 = mutacao(d2, matriz_restricao)

        descendentes.append(d1)
        descendentes.append(d2)

    return descendentes, qd

def moda_pop(pop, tp, desc, qd):
    candidatos = pop + desc

    fit_candidatos = [1.0 / (1.0 + avalia_escala(ind)) for ind in candidatos]

    ordenados = sorted(zip(candidatos, fit_candidatos), key=lambda x: x[1], reverse=True)

    nova_pop = [ind for ind, fit in ordenados[:tp]]

    return nova_pop

def rotina_algoritmo_genetico(n, tp, ng, tm, tc, matriz_restricao):
    # n = número de dias
    # tp = tamanho da população
    # ng = número de gerações
    # tm = taxa de mutação
    # tc = taxa de cruzamento

    #matriz_restricao = gerar_matriz_restricao("A", tp)
    pop = gerar_populacao_inicial(tp, matriz_restricao)
    fit = aptidao(pop)

    for g in range(1, ng+1):
        desc, qd = descendente(n, pop, fit, tp, tc, tm, matriz_restricao)

        pop = moda_pop(pop, tp, desc, qd)
        fit = aptidao(pop)

    melhor = max(zip(pop, fit), key=lambda x: x[1])[0]
    return melhor
