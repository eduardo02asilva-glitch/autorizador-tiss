from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from backend.app.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, index=True)
    numero_carteira = Column(String, nullable=False)
    convenio = Column(String, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)