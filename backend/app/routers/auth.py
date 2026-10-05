from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.usuario import Usuario
from backend.app.models.clinica import Clinica
from backend.app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token
from backend.app.security import gerar_hash_senha, verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/registrar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # 1. Verifica se a clínica existe
    clinica = db.query(Clinica).filter(Clinica.id == usuario.clinica_id).first()
    if not clinica:
        raise HTTPException(
            status_code=404,
            detail="Clínica informada não existe."
        )

    # 2. Verifica se o e-mail já está cadastrado
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado no sistema."
        )

    # 3. Cria o utilizador com a senha encriptada
    novo_usuario = Usuario(
        clinica_id=usuario.clinica_id,
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # O OAuth2PasswordRequestForm recebe 'username' (usaremos como email) e 'password'
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = criar_token_acesso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}