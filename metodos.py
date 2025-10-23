from random import randint
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