from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Date,
    DateTime,
    Enum,
    BigInteger,
    Boolean
)
from database import Base
import enum


class EstadoEnum(str, enum.Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"
    LIBRE = "LIBRE"
    BLOQUEADO = "BLOQUEADO"


class SexoEnum(str, enum.Enum):
    M = "M"
    F = "F"

# Añadir a models.py
class Geografia(Base):
    __tablename__ = "geografia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)


class Interno(Base):
    __tablename__ = "internos"

    id = Column(String(45), primary_key=True, index=True)
    nombres = Column(String(1024), nullable=False)
    apellidos = Column(String(100))
    idUbicacion = Column(Integer, nullable=False)

    cortesia = Column(Float)
    fechaHoraRegistro = Column(BigInteger)
    activo = Column(Boolean)
    clave = Column(String(45))
    fechaNacimiento = Column(Date)

    desarrollo = Column(Boolean, default=False)
    cambiarClave = Column(Boolean, default=False)
    idPerfil = Column(Integer)

    pabellon = Column(String(45))
    piso = Column(String(45))
    ala = Column(String(45))

    estado = Column(Enum(EstadoEnum))
    fechaIngreso = Column(DateTime)
    requeridoAgente = Column(Boolean, default=False)

    sexo = Column(Enum(SexoEnum))
    fechaHoraUltimaLlamada = Column(BigInteger)

    prefijoPenal = Column(Integer)
    identificacion = Column(String(45))
    tratamientoDatos = Column(Integer)
    idGeografia = Column(Integer)


class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombres = Column(String(255), nullable=False)
    clave = Column(String(255), nullable=False)  # En producción, usar hash de contraseña
