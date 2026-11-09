from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_registro_telemetria_valida():
    payload = {
        "id_caminhao": 101,
        "temp_ar_admissao": 28.5,
        "posicao_acelerador": 45.0,
        "tempo_motor_ligado": "01:23",
        "carga_motor": 62.0,
        "rpm_motor": 1850.0,
        "pressao_pneu": 110.0,
        "sensores_oxigenio": 0.85,
        "qtd_combustivel": 78.0,
        "temp_arrefecimento": 88.0,
        "pressao_coletor_admissao": 101.3
    }
    resposta = client.post("/api/v1/telemetria", json=payload)
    assert resposta.status_code == 201
    dados = resposta.json()
    assert dados["id_caminhao"] == 101
    assert dados["status"] == "sucesso"


def test_registro_telemetria_acelerador_invalido():
    # Acelerador acima de 100% deve ser rejeitado pela validação
    payload = {
        "id_caminhao": 101,
        "temp_ar_admissao": 25.0,
        "posicao_acelerador": 150.0,  # Inválido (> 100)
        "tempo_motor_ligado": "00:10",
        "carga_motor": 50.0,
        "rpm_motor": 2000.0,
        "qtd_combustivel": 50.0,
        "temp_arrefecimento": 90.0,
        "pressao_coletor_admissao": 100.0
    }
    resposta = client.post("/api/v1/telemetria", json=payload)
    assert resposta.status_code == 422


def test_consultar_ultimas_leituras():
    resposta = client.get("/api/v1/telemetria/ultimas")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)
