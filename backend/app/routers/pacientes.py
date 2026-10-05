from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.paciente import Paciente
from backend.app.models.clinica import Clinica
from backend.app.schemas.paciente import PacienteCreate, PacienteResponse

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    # Verifica se a clínica informada existe
    clinica = db.query(Clinica).filter(Clinica.id == paciente.clinica_id).first()
    if not clinica:
        raise HTTPException(
            status_code=404, 
            detail="Clínica informada não existe."
        )

    novo_paciente = Paciente(
        clinica_id=paciente.clinica_id,
        nome=paciente.nome,
        cpf=paciente.cpf,
        numero_carteira=paciente.numero_carteira,
        convenio=paciente.convenio
    )
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)
    return novo_paciente

@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()