from random import randint, random
from math import exp
from metodosbasicos import avalia_escala, gerar_matriz_restricao, gerar_solucao_inicial

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
        
def subida_encosta_tentativas(solucao_inicial, avaliacao_inicial, matriz_restricao, t_max):
    atual = [linha[:] for linha in solucao_inicial]
    va = avaliacao_inicial
    tentativa = 0

    while tentativa < t_max:
        novo, vn = sucessores(atual, va, matriz_restricao)
        if vn < va:
            atual = [linha[:] for linha in novo]
            va = vn
            tentativa = 0
        else:
            tentativa += 1

def ganho(avaliacao_inicial, avaliacao_final):
    vi = avaliacao_inicial
    vf = avaliacao_final
    ganho = (100*(vi-vf))/vi

    return ganho

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

def analise_melhor_config():
    ganho[11] = {0}
    n = 20

    for i in range(n):
        matriz_restricao = gerar_matriz_restricao("F")
        si = gerar_solucao_inicial(matriz_restricao)
        vi = avalia_escala(si)

        # subida de encosta
        sf, vf = subida_encosta(si, vi, matriz_restricao)
        ganho[0] += ganho(vi, vf)

        # subida de encosta com tentativas
        tmax = n
        sf, vf = subida_encosta_tentativas(si, vi, matriz_restricao, tmax)
        ganho[1] += ganho(vi, vf)

        tmax = n/2
        sf, vf = subida_encosta_tentativas(si, vi, matriz_restricao, tmax)
        ganho[2] += ganho(vi, vf)

        tmax = n/4
        sf, vf = subida_encosta_tentativas(si, vi, matriz_restricao, tmax)
        ganho[3] += ganho(vi, vf)

        # tempera simulada
        sf, vf = tempera_simulada(si, vi, matriz_restricao, 100, 0.1, 0.8)
        ganho[4] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 200, 0.1, 0.8)
        ganho[5] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 500, 0.1, 0.8)
        ganho[6] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 200, 0.1, 0.9)
        ganho[7] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 500, 0.1, 0.9)
        ganho[8] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 200, 0.01, 0.9)
        ganho[9] += ganho(vi, vf)

        sf, vf = tempera_simulada(si, vi, matriz_restricao, 500, 0.01, 0.9)
        ganho[10] += ganho(vi, vf)

    for i in range(11):
        ganho[i] = ganho[i]/n