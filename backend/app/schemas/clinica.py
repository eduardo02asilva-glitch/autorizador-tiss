from pydantic import BaseModel
from datetime import datetime

# Schema para criação (o que o cliente envia)
class ClinicaCreate(BaseModel):
    nome_fantasia: str
    cnpj: str

# Schema de resposta (o que a API retorna)
class ClinicaResponse(BaseModel):
    id: int
    nome_fantasia: str
    cnpj: str
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True