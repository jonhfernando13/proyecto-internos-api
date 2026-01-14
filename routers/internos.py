from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Interno
from schemas import (
    InternoCreate,
    InternoUpdate,
    InternoResponse
)

router = APIRouter(
    prefix="/internos",
    tags=["Internos"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET ALL
@router.get("/", response_model=list[InternoResponse])
def listar_internos(db: Session = Depends(get_db)):
    return db.query(Interno).all()


# GET ONE
@router.get("/{interno_id}", response_model=InternoResponse)
def obtener_interno(interno_id: str, db: Session = Depends(get_db)):
    interno = db.query(Interno).filter(Interno.id == interno_id).first()
    if not interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")
    return interno


# CREATE
@router.post("/", response_model=InternoResponse)
def crear_interno(
    interno: InternoCreate,
    db: Session = Depends(get_db)
):
    db_interno = Interno(**interno.dict())
    db.add(db_interno)
    db.commit()
    db.refresh(db_interno)
    return db_interno


# UPDATE
@router.put("/{interno_id}", response_model=InternoResponse)
def actualizar_interno(
    interno_id: str,
    datos: InternoUpdate,
    db: Session = Depends(get_db)
):
    interno = db.query(Interno).filter(Interno.id == interno_id).first()
    if not interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(interno, campo, valor)

    db.commit()
    db.refresh(interno)
    return interno


# DELETE
@router.delete("/{interno_id}")
def eliminar_interno(
    interno_id: str,
    db: Session = Depends(get_db)
):
    interno = db.query(Interno).filter(Interno.id == interno_id).first()
    if not interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")

    db.delete(interno)
    db.commit()
    return {"mensaje": "Interno eliminado correctamente"}
