from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from routers.internos import router as internos_router
from routers.geografia import router as geografia_router
from routers.auth import router as auth_router
from database import engine

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Clientes",
    description="API para gestión de internos y geografías",
    version="1.0.0"
)

# CORS - permitir frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers UNA SOLA VEZ
app.include_router(auth_router)
app.include_router(internos_router)
app.include_router(geografia_router)


@app.get("/", tags=["root"])
def read_root():
    """Endpoint raíz"""
    return {"message": "Bienvenido a la API de Clientes"}


@app.get("/health", tags=["health"])
def health_check():
    """Verificar que la API está activa"""
    return {"status": "ok"}