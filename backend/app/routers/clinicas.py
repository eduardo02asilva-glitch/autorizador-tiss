from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.clinica import Clinica
from backend.app.schemas.clinica import ClinicaCreate, ClinicaResponse

router = APIRouter(prefix="/clinicas", tags=["Clínicas"])

@router.post("/", response_model=ClinicaResponse, status_code=status.HTTP_201_CREATED)
def criar_clinica(clinica: ClinicaCreate, db: Session = Depends(get_db)):
    # Verifica se o CNPJ já está cadastrado
    db_clinica = db.query(Clinica).filter(Clinica.cnpj == clinica.cnpj).first()
    if db_clinica:
        raise HTTPException(
            status_code=400, 
            detail="CNPJ já cadastrado no sistema."
        )
    
    nova_clinica = Clinica(
        nome_fantasia=clinica.nome_fantasia,
        cnpj=clinica.cnpj
    )
    db.add(nova_clinica)
    db.commit()
    db.refresh(nova_clinica)
    return nova_clinica

@router.get("/", response_model=List[ClinicaResponse])
def listar_clinicas(db: Session = Depends(get_db)):
    return db.query(Clinica).all()