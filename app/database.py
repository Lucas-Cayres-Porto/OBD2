import logging
from typing import Optional, List, Dict, Any
from app.config import settings

logger = logging.getLogger("obd2.database")

# Estrutura simulada para testes locais/CI sem banco ativo
MOCK_MOTORISTAS = {
    "motorista@transporte.com": {"id": 1, "senha": "senhaSegura123", "email": "motorista@transporte.com"},
    "teste@empresa.com": {"id": 2, "senha": "1234", "email": "teste@empresa.com"},
}

MOCK_VEICULOS = {
    1: [
        {"id": 101, "placa": "ABC-1234", "modelo": "Volvo FH 540"},
        {"id": 102, "placa": "XYZ-9876", "modelo": "Scania R450"},
    ],
    2: [
        {"id": 201, "placa": "JNF-2026", "modelo": "Mercedes-Benz Actros"},
    ],
}

TELEMETRIA_REGISTROS: List[Dict[str, Any]] = []


def verificar_credenciais(email: str, senha: str) -> Optional[int]:
    """
    Verifica se o motorista existe e se a senha confere.
    Usa a base de dados mock/fallback se não houver conexão externa.
    """
    motorista = MOCK_MOTORISTAS.get(email.lower())
    if motorista and motorista["senha"] == senha:
        return motorista["id"]
    return None


def obter_veiculos_por_motorista(id_motorista: int) -> List[Dict[str, Any]]:
    """
    Retorna os veículos vinculados ao id do motorista.
    """
    return MOCK_VEICULOS.get(id_motorista, [
        {"id": 1, "placa": "PADRAO-01", "modelo": "Caminhão Padrão"}
    ])


def inserir_telemetria(dados: Dict[str, Any]) -> Dict[str, Any]:
    """
    Registra os dados de telemetria coletados.
    """
    TELEMETRIA_REGISTROS.append(dados)
    logger.info(f"Telemetria registrada para o caminhão {dados.get('id_caminhao')}")
    return dados
