from random import randint, random
from math import exp
from metodosbasicos import avalia_escala

def subida_encosta(solucao_inicial, avaliacao_inicial, matriz_restricao):
    atual = [linha[:] for linha in solucao_inicial]
    va = avaliacao_inicial

    while True:
        novo, vn = sucessores(atual, va, matriz_restricao)
        if vn < va:
            atual = [linha[:] for linha in novo]
            va = vn
        else:
            return atual, va

def sucessores(s, v, m):
    melhor = [linha[:] for linha in s] 
    vm = v
    funcs = len(s)
    dias = len(s[0])
    i = randint(0, funcs - 1)

    for j in range(funcs):
        for k in range(dias):
            if s[j][k] != s[i][k] and m[i][k] == 1 and m[j][k] == 1:
                aux = [linha[:] for linha in s]  
                aux[i][k], aux[j][k] = aux[j][k], aux[i][k]
                vaux = avalia_escala(aux)
                if vaux < vm:
                    melhor = [linha[:] for linha in aux]
                    vm = vaux
    return melhor, vm

def tempera_simulada(solucao_inicial, avaliacao_inicial, matriz_restricao, ti=100, tf=1, fr=0.9):
    atual = [linha[:] for linha in solucao_inicial]
    va = avaliacao_inicial
    temp = ti
    funcs = len(atual)
    dias = len(atual[0])

    while temp > tf:

        # Gera um vizinho aleatório trocando um dia entre dois funcionários
        novo = [linha[:] for linha in atual]
        i = randint(0, funcs - 1)
        j = randint(0, funcs - 1)
        k = randint(0, dias - 1)

        if i != j and matriz_restricao[i][k] == 1 and matriz_restricao[j][k] == 1:
            novo[i][k], novo[j][k] = novo[j][k], novo[i][k]

        vn = avalia_escala(novo)
        delta = vn - va

        if delta < 0:
            atual = novo
            va = vn
        else:
            aleatorio = random()
            prob = exp(-delta / temp)
            if aleatorio < prob:
                atual = novo
                va = vn

        temp *= fr

    return atual, va

