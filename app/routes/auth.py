from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, LoginResponse
from app.database import verificar_credenciais

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login do Motorista",
    description="Autentica o motorista através do e-mail e senha cadastrados no sistema."
)
def login(dados: LoginRequest):
    id_motorista = verificar_credenciais(dados.email, dados.senha)
    if not id_motorista:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas: e-mail não cadastrado ou senha incorreta."
        )

    return LoginResponse(
        id_motorista=id_motorista,
        email=dados.email,
        mensagem="Login realizado com sucesso!"
    )
