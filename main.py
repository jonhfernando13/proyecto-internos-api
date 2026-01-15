from fastapi import FastAPI
from routers.internos import router as internos_router
from fastapi.middleware.cors import CORSMiddleware
from routers.geografia import router as geografia_router
import models
from database import engine


models.Base.metadata.create_all(bind=engine)



app = FastAPI(title="API Clientes")

app.include_router(internos_router)
app.include_router(geografia_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
