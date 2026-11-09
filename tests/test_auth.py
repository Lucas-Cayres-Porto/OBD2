from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_sucesso():
    payload = {
        "email": "motorista@transporte.com",
        "senha": "senhaSegura123"
    }
    resposta = client.post("/api/v1/auth/login", json=payload)
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["id_motorista"] == 1
    assert dados["email"] == "motorista@transporte.com"


def test_login_senha_incorreta():
    payload = {
        "email": "motorista@transporte.com",
        "senha": "senhaErrada"
    }
    resposta = client.post("/api/v1/auth/login", json=payload)
    assert resposta.status_code == 401
    assert "Credenciais inválidas" in resposta.json()["detail"]


def test_login_email_invalido_formato():
    payload = {
        "email": "email_sem_arroba_ponto_com",
        "senha": "1234"
    }
    resposta = client.post("/api/v1/auth/login", json=payload)
    # Validação do Pydantic deve barrar e retornar 422
    assert resposta.status_code == 422


def test_listar_veiculos_motorista():
    resposta = client.get("/api/v1/veiculos/1")
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["id_motorista"] == 1
    assert dados["total"] >= 1
    assert len(dados["veiculos"]) >= 1
