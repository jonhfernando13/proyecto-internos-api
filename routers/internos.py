from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models
import schemas


router = APIRouter(prefix="/internos", tags=["internos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.InternoResponse])
def get_internos(db: Session = Depends(get_db)):
    """Obtener todos los internos"""
    internos = db.query(models.Interno).all()
    return internos


@router.get("/{interno_id}", response_model=schemas.InternoResponse)
def get_interno(interno_id: str, db: Session = Depends(get_db)):
    """Obtener un interno por ID"""
    interno = db.query(models.Interno).filter(models.Interno.id == interno_id).first()
    if not interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")
    return interno


@router.post("/", response_model=schemas.InternoResponse)
def create_interno(interno: schemas.InternoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo interno"""
    db_interno = models.Interno(**interno.dict())
    db.add(db_interno)
    db.commit()
    db.refresh(db_interno)
    return db_interno


@router.put("/{interno_id}", response_model=schemas.InternoResponse)
def update_interno(interno_id: str, interno: schemas.InternoUpdate, db: Session = Depends(get_db)):
    """Actualizar un interno"""
    db_interno = db.query(models.Interno).filter(models.Interno.id == interno_id).first()
    if not db_interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")
    
    update_data = interno.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_interno, key, value)
    
    db.commit()
    db.refresh(db_interno)
    return db_interno


@router.delete("/{interno_id}")
def delete_interno(interno_id: str, db: Session = Depends(get_db)):
    """Eliminar un interno"""
    db_interno = db.query(models.Interno).filter(models.Interno.id == interno_id).first()
    if not db_interno:
        raise HTTPException(status_code=404, detail="Interno no encontrado")
    
    db.delete(db_interno)
    db.commit()
    return {"message": "Interno eliminado correctamente"}
