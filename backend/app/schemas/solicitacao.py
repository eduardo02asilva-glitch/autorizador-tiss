from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema para criação da solicitação
class SolicitacaoCreate(BaseModel):
    clinica_id: int
    paciente_id: int
    procedimento: str

# Schema para atualização de status (ex: autorizar ou negar)
class SolicitacaoUpdateStatus(BaseModel):
    status: str  # pendente, autorizada, negada

# Schema de resposta da API
class SolicitacaoResponse(BaseModel):
    id: int
    clinica_id: int
    paciente_id: int
    procedimento: str
    status: str
    criado_em: datetime

    class Config:
        from_attributes = True