import os
import re
import logging
import warnings
from datetime import datetime
from time import sleep
import httpx
from dotenv import load_dotenv
import cores as c

try:
    import obd
    logging.getLogger("obd.obd").setLevel(logging.CRITICAL)
except ImportError:
    obd = None

warnings.filterwarnings("ignore")
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def efetuarLogin(client: httpx.Client) -> int:
    """Solicita credenciais do motorista e valida na API FastAPI."""
    c.separador()
    print(f"{c.branco_negrito}Faça o Seu Login{c.reset}".center(70))
    c.separador()

    while True:
        while True:
            email = input("Digite o seu email: ")
            if re.match(r"^[A-Za-z0-9\.-]+@[a-zA-Z]+\.[A-Za-z\.]+$", email):
                break
            else:
                print(f"{c.vermelho}Formato de email inválido, digite um válido!{c.reset}")

        senha = input("Digite a sua senha: ")

        try:
            resposta = client.post(
                f"{API_BASE_URL}/api/v1/auth/login",
                json={"email": email, "senha": senha},
                timeout=10.0,
            )
            if resposta.status_code == 200:
                dados = resposta.json()
                c.separador()
                print(f"{c.verde_negrito}Login realizado com sucesso !{c.reset}".center(70))
                c.separador()
                return dados["id_motorista"]
            elif resposta.status_code == 401:
                print(f"{c.vermelho}Credenciais inválidas: e-mail não cadastrado ou senha incorreta!{c.reset}")
                c.separador()
            else:
                print(f"{c.vermelho}Erro na autenticação ({resposta.status_code}): {resposta.text}{c.reset}")
                c.separador()
        except httpx.ConnectError:
            print(f"{c.vermelho}Não foi possível conectar à API em {API_BASE_URL}. Verifique se o servidor está ativo!{c.reset}")
        except Exception as e:
            print(f"{c.vermelho}Erro ao comunicar com a API: {e}{c.reset}")


def escolherVeiculo(id_motorista: int, client: httpx.Client) -> int:
    """Consulta veículos vinculados ao motorista via API FastAPI e permite seleção."""
    try:
        resposta = client.get(
            f"{API_BASE_URL}/api/v1/veiculos/{id_motorista}",
            timeout=10.0,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        veiculos = dados.get("veiculos", [])
    except Exception as e:
        print(f"{c.vermelho}Erro ao consultar veículos na API: {e}{c.reset}")
        return 1

    if not veiculos:
        print(f"{c.vermelho}Nenhum veículo vinculado a este motorista!{c.reset}")
        return 1

    c.separador()
    print(f"{c.branco_negrito}Veículos Disponíveis{c.reset}".center(70))
    for i, veiculo in enumerate(veiculos):
        print(
            f"{c.branco_negrito}{i+1}{c.reset} - "
            f"Placa: {c.amarelo}{veiculo['placa']}{c.reset}, "
            f"Modelo: {c.amarelo}{veiculo['modelo']}{c.reset}"
        )

    while True:
        try:
            escolha = int(input("Escolha um dos veículos: "))
            if 1 <= escolha <= len(veiculos):
                break
            print(f"{c.vermelho}Escolha um número entre 1 e {len(veiculos)}{c.reset}")
        except ValueError:
            print(f"{c.vermelho}Digite um número válido!{c.reset}")

    c.separador()
    print(f"{c.verde_negrito}Veículo escolhido com sucesso !{c.reset}".center(70))
    c.separador()
    return veiculos[escolha - 1]["id"]


def extrair_valor(query_result, default: float = -1.0) -> float:
    """Extrai valor numérico seguro de uma leitura OBD."""
    if query_result is None or query_result.is_null():
        return default
    try:
        val = query_result.value
        return float(val.magnitude) if hasattr(val, "magnitude") else float(val)
    except (AttributeError, ValueError, TypeError):
        return default


def coletar_e_enviar(id_caminhao: int, conexao_obd, client: httpx.Client) -> bool:
    """Lê os sensores do scanner OBD e envia o payload para o endpoint de telemetria da API."""
    if obd and conexao_obd is not None and getattr(conexao_obd, "is_connected", lambda: False)():
        temp_ar = extrair_valor(conexao_obd.query(obd.commands.INTAKE_TEMP))
        raw_throttle = extrair_valor(conexao_obd.query(obd.commands.THROTTLE_POS), default=0.0)
        pos_acelerador = max(0.0, min(100.0, raw_throttle))
        run_time_query = conexao_obd.query(obd.commands.RUN_TIME)
        tempo_motor = "00:00" if run_time_query.is_null() else str(run_time_query.value)
        carga_motor = extrair_valor(conexao_obd.query(obd.commands.ENGINE_LOAD))
        rpm = extrair_valor(conexao_obd.query(obd.commands.RPM))
        o2_sensor = extrair_valor(conexao_obd.query(obd.commands.O2_B1S1))
        combustivel = extrair_valor(conexao_obd.query(obd.commands.FUEL_LEVEL))
        temp_arrefecimento = extrair_valor(conexao_obd.query(obd.commands.COOLANT_TEMP))
        pressao_coletor = extrair_valor(conexao_obd.query(obd.commands.INTAKE_PRESSURE))
    else:
        temp_ar = -1.0
        pos_acelerador = 0.0
        tempo_motor = "00:00"
        carga_motor = -1.0
        rpm = -1.0
        o2_sensor = -1.0
        combustivel = -1.0
        temp_arrefecimento = -1.0
        pressao_coletor = -1.0

    payload = {
        "id_caminhao": id_caminhao,
        "temp_ar_admissao": temp_ar,
        "posicao_acelerador": pos_acelerador,
        "tempo_motor_ligado": tempo_motor,
        "carga_motor": carga_motor,
        "rpm_motor": rpm,
        "dt_hora_leitura": datetime.now().isoformat(),
        "pressao_pneu": -1.0,
        "sensores_oxigenio": o2_sensor,
        "qtd_combustivel": combustivel,
        "temp_arrefecimento": temp_arrefecimento,
        "pressao_coletor_admissao": pressao_coletor,
    }

    try:
        resposta = client.post(
            f"{API_BASE_URL}/api/v1/telemetria",
            json=payload,
            timeout=10.0,
        )
        if resposta.status_code == 201:
            return True
        else:
            print(f"{c.vermelho}Erro ao registrar telemetria ({resposta.status_code}): {resposta.text}{c.reset}")
            return False
    except httpx.ConnectError:
        print(f"{c.vermelho}[Offline] Falha ao conectar à API em {API_BASE_URL}. Verifique a conexão.{c.reset}")
        return False
    except Exception as e:
        print(f"{c.vermelho}Erro no envio da telemetria: {e}{c.reset}")
        return False


def main(total_leituras: int = 10, intervalo_segundos: int = 10):
    with httpx.Client() as client:
        id_motorista = efetuarLogin(client)
        id_caminhao = escolherVeiculo(id_motorista, client)

        c.separador()
        print(f"{c.branco_negrito}Iniciando Coleta de Dados OBD2{c.reset}".center(70))

        conexao_obd = None
        if obd:
            try:
                conexao_obd = obd.OBD()
                if not conexao_obd.is_connected():
                    print(f"{c.amarelo}Aviso: Scanner OBD2 não detectado. Operando em modo de leitura padrão.{c.reset}")
            except Exception as e:
                print(f"{c.amarelo}Aviso: Não foi possível conectar ao scanner OBD2 ({e}). Modo padrão ativo.{c.reset}")

        for i in range(total_leituras):
            sleep(intervalo_segundos)
            sucesso = coletar_e_enviar(id_caminhao, conexao_obd, client)
            status_msg = f"{c.verde}Sucesso{c.reset}" if sucesso else f"{c.vermelho}Falha{c.reset}"
            print(f"{c.ciano}Coleta de Dados: {i+1}/{total_leituras} -> {status_msg}")

        if conexao_obd and hasattr(conexao_obd, "close"):
            conexao_obd.close()

        c.separador()
        print(f"{c.verde_negrito}Ciclo de Coleta Realizado com Sucesso{c.reset}".center(70))
        c.separador()


if __name__ == "__main__":
    main()
