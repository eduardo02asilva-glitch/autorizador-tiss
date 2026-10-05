import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.routers import auth, clinicas, pacientes, solicitacoes
from backend.app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autorizador TISS", version="1.0.0")

# Routers
app.include_router(auth.router)
app.include_router(clinicas.router)
app.include_router(pacientes.router)
app.include_router(solicitacoes.router)

# Configuração de Arquivos Estáticos (Frontend)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def servir_dashboard():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health", tags=["default"])
def health_check():
    return {"status": "ok", "message": "API do Autorizador TISS operando normalmente."}