from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models
import schemas


class EstadoEnum(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    LIBRE = "LIBRE"
    BLOQUEADO = "BLOQUEADO"


class SexoEnum(str, Enum):
    M = "M"
    F = "F"

# Añadir a schemas.py
class GeografiaBase(BaseModel):
    id: int
    nombre: str

class GeografiaResponse(GeografiaBase):
    class Config:
        from_attributes = True


class InternoBase(BaseModel):
    id: str
    nombres: str
    apellidos: Optional[str] = None
    idUbicacion: int

    cortesia: Optional[float] = None
    fechaHoraRegistro: Optional[int] = None
    activo: Optional[bool] = None
    clave: Optional[str] = None
    fechaNacimiento: Optional[date] = None

    desarrollo: Optional[bool] = False
    cambiarClave: Optional[bool] = False
    idPerfil: Optional[int] = None

    pabellon: Optional[str] = None
    piso: Optional[str] = None
    ala: Optional[str] = None

    estado: Optional[EstadoEnum] = None
    fechaIngreso: Optional[datetime] = None
    requeridoAgente: Optional[bool] = False

    sexo: Optional[SexoEnum] = None
    fechaHoraUltimaLlamada: Optional[int] = None

    prefijoPenal: Optional[int] = None
    identificacion: Optional[str] = None
    tratamientoDatos: Optional[int] = None
    idGeografia: Optional[int] = None


class InternoCreate(InternoBase):
    pass


class InternoUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    idUbicacion: Optional[int] = None

    cortesia: Optional[float] = None
    fechaHoraRegistro: Optional[int] = None
    activo: Optional[bool] = None
    clave: Optional[str] = None
    fechaNacimiento: Optional[date] = None

    desarrollo: Optional[bool] = None
    cambiarClave: Optional[bool] = None
    idPerfil: Optional[int] = None

    pabellon: Optional[str] = None
    piso: Optional[str] = None
    ala: Optional[str] = None

    estado: Optional[EstadoEnum] = None
    fechaIngreso: Optional[datetime] = None
    requeridoAgente: Optional[bool] = None

    sexo: Optional[SexoEnum] = None
    fechaHoraUltimaLlamada: Optional[int] = None

    prefijoPenal: Optional[int] = None
    identificacion: Optional[str] = None
    tratamientoDatos: Optional[int] = None
    idGeografia: Optional[int] = None


class InternoResponse(InternoBase):
    class Config:
        from_attributes = True


# Schemas de autenticación
class LoginRequest(BaseModel):
    nombres: str
    clave: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict
