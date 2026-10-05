from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from backend.app.database import get_db
from backend.app.models.solicitacao import Solicitacao
from backend.app.models.clinica import Clinica
from backend.app.models.paciente import Paciente
from backend.app.models.usuario import Usuario
from backend.app.schemas.solicitacao import (
    SolicitacaoCreate, 
    SolicitacaoResponse, 
    SolicitacaoUpdateStatus
)
from backend.app.security import obter_usuario_atual
from backend.app.services.tiss_xml import gerar_xml_guia_sps_sadt, validar_estrutura_xml_tiss

router = APIRouter(prefix="/solicitacoes", tags=["Solicitações TISS"])

@router.post("/", response_model=SolicitacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_solicitacao(
    solicitacao: SolicitacaoCreate, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)  # Rota protegida
):
    clinica = db.query(Clinica).filter(Clinica.id == solicitacao.clinica_id).first()
    if not clinica:
        raise HTTPException(
            status_code=404, 
            detail="Clínica informada não existe."
        )

    paciente = db.query(Paciente).filter(
        Paciente.id == solicitacao.paciente_id,
        Paciente.clinica_id == solicitacao.clinica_id
    ).first()
    
    if not paciente:
        raise HTTPException(
            status_code=404, 
            detail="Paciente não encontrado ou não pertence a esta clínica."
        )

    nova_solicitacao = Solicitacao(
        clinica_id=solicitacao.clinica_id,
        paciente_id=solicitacao.paciente_id,
        procedimento=solicitacao.procedimento,
        status="pendente"
    )
    
    db.add(nova_solicitacao)
    db.commit()
    db.refresh(nova_solicitacao)
    return nova_solicitacao

@router.get("/", response_model=List[SolicitacaoResponse])
def listar_solicitacoes(
    clinica_id: int = None, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)  # Rota protegida
):
    query = db.query(Solicitacao)
    if clinica_id:
        query = query.filter(Solicitacao.clinica_id == clinica_id)
    return query.all()

@router.get("/{solicitacao_id}", response_model=SolicitacaoResponse)
def buscar_solicitacao(
    solicitacao_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)  # Rota protegida
):
    solicitacao = db.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    if not solicitacao:
        raise HTTPException(
            status_code=404, 
            detail="Solicitação TISS não encontrada."
        )
    return solicitacao

@router.patch("/{solicitacao_id}/status", response_model=SolicitacaoResponse)
def atualizar_status_solicitacao(
    solicitacao_id: int, 
    status_data: SolicitacaoUpdateStatus, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)  # Rota protegida
):
    solicitacao = db.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    if not solicitacao:
        raise HTTPException(
            status_code=404, 
            detail="Solicitação TISS não encontrada."
        )

    status_permitidos = ["pendente", "autorizada", "negada"]
    if status_data.status.lower() not in status_permitidos:
        raise HTTPException(
            status_code=400,
            detail=f"Status inválido. Escolha entre: {', '.join(status_permitidos)}"
        )

    solicitacao.status = status_data.status.lower()
    db.commit()
    db.refresh(solicitacao)
    return solicitacao

@router.get("/{solicitacao_id}/xml")
def exportar_xml_solicitacao(
    solicitacao_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    solicitacao = db.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    if not solicitacao:
        raise HTTPException(
            status_code=404, 
            detail="Solicitação TISS não encontrada."
        )

    paciente = db.query(Paciente).filter(Paciente.id == solicitacao.paciente_id).first()

    dados_xml = {
        "id": solicitacao.id,
        "clinica_id": solicitacao.clinica_id,
        "paciente_carteira": paciente.numero_carteira if paciente else "N/A",
        "procedimento": solicitacao.procedimento
    }

    conteudo_xml = gerar_xml_guia_sps_sadt(dados_xml)

    return Response(
        content=conteudo_xml, 
        media_type="application/xml",
        headers={"Content-Disposition": f"attachment; filename=guia_tiss_{solicitacao_id}.xml"}
    )

@router.post("/validar-xml")
async def validar_xml_tiss_upload(
    file: UploadFile = File(...),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    if not file.filename.endswith('.xml'):
        raise HTTPException(
            status_code=400, 
            detail="Apenas ficheiros com extensão .xml são aceites."
        )

    conteudo = await file.read()
    valido, mensagem = validar_estrutura_xml_tiss(conteudo.decode('utf-8'))

    if not valido:
        raise HTTPException(
            status_code=422,
            detail={"status": "inválido", "erro": mensagem}
        )

    return {
        "status": "válido",
        "nome_arquivo": file.filename,
        "mensagem": mensagem
    }