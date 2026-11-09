from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import re


EMAIL_REGEX = r"^[A-Za-z0-9\.-]+@[a-zA-Z]+\.[A-Za-z\.]+$"


class LoginRequest(BaseModel):
    email: str = Field(..., description="E-mail do motorista")
    senha: str = Field(..., min_length=4, description="Senha do motorista")

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Formato de email inválido! Exemplo aceito: motorista@empresa.com")
        return v


class LoginResponse(BaseModel):
    id_motorista: int
    email: str
    mensagem: str = "Login realizado com sucesso!"


class Veiculo(BaseModel):
    id: int
    placa: str
    modelo: str


class VeiculosResponse(BaseModel):
    id_motorista: int
    total: int
    veiculos: List[Veiculo]


class TelemetriaInput(BaseModel):
    id_caminhao: int = Field(..., gt=0, description="Identificador do veículo/caminhão")
    temp_ar_admissao: float = Field(..., description="Temperatura do ar de admissão em °C")
    posicao_acelerador: float = Field(..., ge=0.0, le=100.0, description="Posição do acelerador (0-100%)")
    tempo_motor_ligado: str = Field(default="00:00", description="Tempo de funcionamento do motor")
    carga_motor: float = Field(..., ge=-1.0, le=100.0, description="Carga calculada do motor (-1 ou 0-100%)")
    rpm_motor: float = Field(..., ge=-1.0, le=12000.0, description="Rotações por minuto do motor")
    dt_hora_leitura: Optional[datetime] = Field(default_factory=datetime.now, description="Data e hora da leitura")
    pressao_pneu: float = Field(default=-1.0, description="Pressão dos pneus em PSI")
    sensores_oxigenio: float = Field(default=-1.0, description="Leitura dos sensores de oxigênio O2")
    qtd_combustivel: float = Field(..., ge=-1.0, le=100.0, description="Nível de combustível em %")
    temp_arrefecimento: float = Field(..., description="Temperatura do líquido de arrefecimento em °C")
    pressao_coletor_admissao: float = Field(..., description="Pressão absoluta do coletor de admissão (MAP)")


class TelemetriaResponse(BaseModel):
    id_caminhao: int
    dt_hora_leitura: datetime
    status: str = "sucesso"
    mensagem: str = "Dados de telemetria OBD2 registrados com sucesso!"
