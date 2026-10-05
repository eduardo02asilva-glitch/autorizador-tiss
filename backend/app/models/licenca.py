from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from backend.app.database import Base

class Licenca(Base):
    __tablename__ = "licencas"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    chave_licenca = Column(String, unique=True, nullable=False, index=True)
    valida_ate = Column(DateTime, nullable=False)
    ativa = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)