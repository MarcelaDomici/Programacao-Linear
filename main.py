from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from metodosbasicos import gerar_matriz_restricao, gerar_solucao_inicial, avalia_escala
from metodos import subida_encosta
app = FastAPI()

estado_escala = {
    "matriz": None,
    "escala": None,
    "avaliacao": None
}

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
    escala = estado_escala["escala"]
    avaliacao = estado_escala["avaliacao"]

    escala_final, avaliacao_final = subida_encosta(escala, avaliacao, matriz_restricao)

    return {
        "escala_final": escala_final,
        "avaliacao_final": avaliacao_final
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