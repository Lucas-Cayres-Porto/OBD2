from fastapi import APIRouter, status
from typing import List, Dict, Any
from datetime import datetime
from app.schemas import TelemetriaInput, TelemetriaResponse
from app.database import inserir_telemetria, TELEMETRIA_REGISTROS

router = APIRouter(prefix="/api/v1/telemetria", tags=["Telemetria OBD2"])


@router.post(
    "",
    response_model=TelemetriaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar Leitura de Sensores OBD2",
    description="Recebe o payload de telemetria lido pelo scanner OBD2 (RPM, velocidade, temperatura, combustível, etc.) e armazena no sistema."
)
def registrar_telemetria(dados: TelemetriaInput):
    payload = dados.model_dump()
    if not payload.get("dt_hora_leitura"):
        payload["dt_hora_leitura"] = datetime.now()

    inserir_telemetria(payload)

    return TelemetriaResponse(
        id_caminhao=dados.id_caminhao,
        dt_hora_leitura=payload["dt_hora_leitura"],
        status="sucesso",
        mensagem="Dados de telemetria OBD2 registrados com sucesso!"
    )


@router.get(
    "/ultimas",
    response_model=List[Dict[str, Any]],
    summary="Consultar Últimas Leituras",
    description="Retorna o histórico recente de telemetria coletada."
)
def obter_ultimas_leituras():
    return TELEMETRIA_REGISTROS[-10:]
