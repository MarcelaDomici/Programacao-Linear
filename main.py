from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from metodosbasicos import gerar_matriz_restricao, gerar_solucao_inicial, avalia_escala
from metodos import subida_encosta, tempera_simulada, ganho, subida_encosta_tentativas, analise_melhor_config
from algoritmosgeneticos import rotina_algoritmo_genetico
app = FastAPI()

estado_escala = {
    "matriz": None,
    "escala": None,
    "avaliacao": None
}

@app.get("/api/analise_melhor_config")
def analise_melhor_config_endpoint():
    resultado = analise_melhor_config()
    return {"ganho": resultado}


@app.get("/api/gerar_escala")
def gerar_escala_endpoint(tipo: str = "A", funcs: int = 3):
    matriz_restricao = gerar_matriz_restricao(tipo, funcs)
    escala = gerar_solucao_inicial(matriz_restricao)
    avaliacao = avalia_escala(escala)

    estado_escala["matriz"] = matriz_restricao
    estado_escala["escala"] = escala
    estado_escala["avaliacao"] = avaliacao

    return {
        "escala": escala,
        "avaliacao": avaliacao,
    }

@app.get("/api/subida_encosta")
def subida_encosta_endpoint():
    if estado_escala["matriz"] is None:
        return {
            "erro": "Nenhuma escala foi gerada ainda. Gere a solução inicial primeiro."
        }

    matriz_restricao = estado_escala["matriz"]
    escala_inicial = estado_escala["escala"]
    avaliacao_inicial = estado_escala["avaliacao"]

    escala_final, avaliacao_final = subida_encosta(escala_inicial, avaliacao_inicial, matriz_restricao)

    ganho_resultado = ganho(avaliacao_inicial, avaliacao_final)

    return {
        "escala_inicial": escala_inicial,
        "avaliacao_inicial": avaliacao_inicial,
        "escala_final": escala_final,
        "avaliacao_final": avaliacao_final,
        "ganho": ganho_resultado
    }

@app.get("/api/tempera_simulada")
def tempera_simulada_endpoint(ti: float, tf: float, fr: float):
    if estado_escala["matriz"] is None:
        return {
            "erro": "Nenhuma escala foi gerada ainda. Gere a solução inicial primeiro."
        }
    
    if ti is None or tf is None or fr is None:
        return {"erro": "Por favor, preencha todos os parâmetros (ti, tf e fr) antes de executar."}

    matriz_restricao = estado_escala["matriz"]
    escala_inicial = estado_escala["escala"]
    avaliacao_inicial = estado_escala["avaliacao"]

    escala_final, avaliacao_final = tempera_simulada(
        escala_inicial, avaliacao_inicial, matriz_restricao, ti, tf=tf, fr=fr
    )

    ganho_resultado = ganho(avaliacao_inicial, avaliacao_final)

    return {
        "escala_inicial": escala_inicial,
        "avaliacao_inicial": avaliacao_inicial,
        "escala_final": escala_final,
        "avaliacao_final": avaliacao_final,
        "ganho": ganho_resultado
    }

@app.get("/api/subida_encosta_tentativas")
def subida_encosta_tentativas_endpoint(t_max: int):
    if estado_escala["matriz"] is None:
        return {
            "erro": "Nenhuma escala foi gerada ainda. Gere a solução inicial primeiro."
        }
    
    if t_max is None:
        return {"erro": "Por favor, preencha o parâmetro (tmax) antes de executar."}
    
    matriz_restricao = estado_escala["matriz"]
    escala_inicial = estado_escala["escala"]
    avaliacao_inicial = estado_escala["avaliacao"]

    escala_final, avaliacao_final = subida_encosta_tentativas(escala_inicial, avaliacao_inicial, matriz_restricao, t_max=t_max)

    ganho_resultado = ganho(avaliacao_inicial, avaliacao_final)

    return {
        "escala_inicial": escala_inicial,
        "avaliacao_inicial": avaliacao_inicial,
        "escala_final": escala_final,
        "avaliacao_final": avaliacao_final,
        "ganho": ganho_resultado
    }

@app.get("/api/algoritmo_genetico")
def algoritmo_genetico_endpoint(n: int, tp: int, ng: int, tm: float, tc: float):
    if estado_escala["matriz"] is None:
        return {"erro": "Nenhuma matriz foi gerada ainda. Gere a solução inicial primeiro."}

    matriz_restricao = estado_escala["matriz"]

    melhor = rotina_algoritmo_genetico(n, tp, ng, tm, tc, matriz_restricao)
    avaliacao = float(avalia_escala(melhor))

    estado_escala["escala"] = melhor
    estado_escala["avaliacao"] = avaliacao

    return {
        "melhor_individuo": melhor,
        "avaliacao": avaliacao
    }

#Endpoints para as páginas HTML

@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("menu.html")

@app.get("/metodoBasico.html", response_class=HTMLResponse)
async def metodo_basico():
    return FileResponse("metodoBasico.html")

@app.get("/algoritmoGenetico.html", response_class=HTMLResponse)
async def algoritmo_genetico():
    return FileResponse("algoritmoGenetico.html")

@app.get("/sobre.html", response_class=HTMLResponse)
async def sobre():
    return FileResponse("sobre.html")

@app.get("/menu.html", response_class=HTMLResponse)
async def home():
    return FileResponse("menu.html")

#Arquivos estáticos
app.mount("/CSS", StaticFiles(directory="CSS"), name="css")