from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_raiz_status_code_e_conteudo():
    resposta = client.get("/")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["status"] == "online"
    assert dados["docs"] == "/docs"
    assert "OBD2" in dados["sistema"]


def test_healthcheck_endpoint():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["status"] == "healthy"
    assert dados["version"] == "1.0.0"
