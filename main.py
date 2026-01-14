from fastapi import FastAPI
from routers.internos import router as internos_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Clientes")

app.include_router(internos_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
