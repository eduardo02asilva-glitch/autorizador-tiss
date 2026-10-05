from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioCreate(BaseModel):
    clinica_id: int
    nome: str
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    clinica_id: int
    nome: str
    email: str
    ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str