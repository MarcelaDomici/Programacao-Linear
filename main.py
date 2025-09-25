from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from metodosbasicos import gerar_matriz_restricao, gerar_solucao_inicial, avalia_escala

app = FastAPI()

@app.get("/api/gerar_escala")
def gerar_escala_endpoint(tipo: str = "A", funcs: int = 3):
    matriz_restricao = gerar_matriz_restricao(tipo, funcs)
    escala = gerar_solucao_inicial(matriz_restricao)
    avaliacao = avalia_escala(escala)

    return {
        "escala": escala,
        "avaliacao": avaliacao,
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