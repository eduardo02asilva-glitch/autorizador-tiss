from pydantic import BaseModel
from datetime import datetime

# Schema para criação
class PacienteCreate(BaseModel):
    clinica_id: int
    nome: str
    cpf: str
    numero_carteira: str
    convenio: str

# Schema de resposta
class PacienteResponse(BaseModel):
    id: int
    clinica_id: int
    nome: str
    cpf: str
    numero_carteira: str
    convenio: str
    criado_em: datetime

    class Config:
        from_attributes = True