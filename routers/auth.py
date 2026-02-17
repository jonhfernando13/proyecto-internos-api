from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from datetime import datetime, timedelta
import secrets

router = APIRouter(
    prefix="/auth",
    tags=["autenticación"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de autenticación para internos y usuarios.
    Valida credenciales contra la base de datos y retorna un token.
    Busca primero en la tabla de internos, luego en usuarios.
    """
    # Primero buscar en la tabla de internos
    interno = db.query(models.Interno).filter(
        models.Interno.nombres == login_data.nombres
    ).first()
    
    if interno and interno.clave == login_data.clave:
        # Autenticación exitosa como interno
        access_token = secrets.token_urlsafe(32)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": interno.id,
                "nombres": interno.nombres,
                "tipo": "interno"
            }
        }
    
    # Si no se encontró como interno, buscar en usuarios
    usuario = db.query(models.Usuario).filter(
        models.Usuario.nombres == login_data.nombres
    ).first()
    
    if usuario and usuario.clave == login_data.clave:
        # Autenticación exitosa como usuario
        access_token = secrets.token_urlsafe(32)
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": usuario.id,
                "nombres": usuario.nombres,
                "tipo": "usuario"
            }
        }
    
    # Si no se encontró en ninguna tabla o las credenciales son incorrectas
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para registrar nuevos usuarios (temporal para pruebas).
    """
    # Verificar si el usuario ya existe
    existing_user = db.query(models.Usuario).filter(
        models.Usuario.nombres == login_data.nombres
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe"
        )
    
    # Crear nuevo usuario
    new_user = models.Usuario(
        nombres=login_data.nombres,
        clave=login_data.clave  # En producción, hashear la contraseña
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Usuario creado exitosamente",
        "user": {
            "id": new_user.id,
            "nombres": new_user.nombres
        }
    }
