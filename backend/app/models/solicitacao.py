from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from backend.app.database import Base

class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    procedimento = Column(String, nullable=False)
    status = Column(String, default="pendente")  # pendente, autorizada, negada
    criado_em = Column(DateTime, default=datetime.utcnow)