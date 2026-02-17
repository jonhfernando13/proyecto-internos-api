from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models
import schemas


router = APIRouter(prefix="/geografia", tags=["geografia"])
 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.GeografiaResponse])
def get_geografias(db: Session = Depends(get_db)):
    """Obtener todas las geografías"""
    geografias = db.query(models.Geografia).all()
    return geografias


@router.get("/{geografia_id}", response_model=schemas.GeografiaResponse)
def get_geografia(geografia_id: int, db: Session = Depends(get_db)):
    """Obtener una geografía por ID"""
    geografia = db.query(models.Geografia).filter(models.Geografia.id == geografia_id).first()
    if not geografia:
        raise HTTPException(status_code=404, detail="Geografía no encontrada")
    return geografia


@router.post("/", response_model=schemas.GeografiaResponse)
def create_geografia(geografia: schemas.GeografiaBase, db: Session = Depends(get_db)):
    """Crear una nueva geografía"""
    db_geografia = models.Geografia(**geografia.dict())
    db.add(db_geografia)
    db.commit()
    db.refresh(db_geografia)
    return db_geografia
