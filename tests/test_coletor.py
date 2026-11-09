from unittest.mock import MagicMock, patch
import httpx
from coletaDadosOBD2 import extrair_valor, coletar_e_enviar, escolherVeiculo, efetuarLogin


def test_extrair_valor_normal():
    mock_result = MagicMock()
    mock_result.is_null.return_value = False
    mock_val = MagicMock()
    mock_val.magnitude = 85.5
    mock_result.value = mock_val

    assert extrair_valor(mock_result) == 85.5


def test_extrair_valor_nulo():
    mock_result = MagicMock()
    mock_result.is_null.return_value = True
    assert extrair_valor(mock_result, default=-1.0) == -1.0


def test_extrair_valor_sem_magnitude():
    mock_result = MagicMock()
    mock_result.is_null.return_value = False
    mock_result.value = 120
    assert extrair_valor(mock_result) == 120.0


def test_coletar_e_enviar_sucesso():
    mock_client = MagicMock(spec=httpx.Client)
    mock_resposta = MagicMock(spec=httpx.Response)
    mock_resposta.status_code = 201
    mock_client.post.return_value = mock_resposta

    sucesso = coletar_e_enviar(id_caminhao=101, conexao_obd=None, client=mock_client)
    assert sucesso is True
    assert mock_client.post.called
    args, kwargs = mock_client.post.call_args
    assert "/api/v1/telemetria" in args[0]
    payload = kwargs["json"]
    assert payload["id_caminhao"] == 101
    assert payload["temp_ar_admissao"] == -1.0


def test_coletar_e_enviar_erro_conexao():
    mock_client = MagicMock(spec=httpx.Client)
    mock_client.post.side_effect = httpx.ConnectError("Falha de rede")

    sucesso = coletar_e_enviar(id_caminhao=101, conexao_obd=None, client=mock_client)
    assert sucesso is False


@patch("builtins.input", return_value="1")
def test_escolher_veiculo(mock_input):
    mock_client = MagicMock(spec=httpx.Client)
    mock_resposta = MagicMock(spec=httpx.Response)
    mock_resposta.raise_for_status.return_value = None
    mock_resposta.json.return_value = {
        "id_motorista": 1,
        "total": 1,
        "veiculos": [{"id": 105, "placa": "TEST-123", "modelo": "Volvo FH"}]
    }
    mock_client.get.return_value = mock_resposta

    id_veiculo = escolherVeiculo(1, mock_client)
    assert id_veiculo == 105


@patch("builtins.input", side_effect=["motorista@transporte.com", "senhaSegura123"])
def test_efetuar_login_sucesso(mock_input):
    mock_client = MagicMock(spec=httpx.Client)
    mock_resposta = MagicMock(spec=httpx.Response)
    mock_resposta.status_code = 200
    mock_resposta.json.return_value = {
        "id_motorista": 1,
        "email": "motorista@transporte.com",
        "mensagem": "Login realizado com sucesso!"
    }
    mock_client.post.return_value = mock_resposta

    id_motorista = efetuarLogin(mock_client)
    assert id_motorista == 1
