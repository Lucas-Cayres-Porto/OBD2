# 🚛 OBD2 - Telemetria Veicular & API REST

Sistema moderno de telemetria automotiva via protocolo OBD2 com ingestão de dados em tempo real, desenvolvido em Python e **FastAPI**.

---

## 🎯 Objetivo do Projeto
Permitir a captura, validação e persistência de dados de telemetria de frotas de caminhões e veículos pesados, disponibilizando:
- Autenticação e identificação de motoristas.
- Vinculação e seleção de veículos da frota.
- Ingestão contínua de parâmetros críticos do motor (RPM, temperatura de admissão, arrefecimento, posição do acelerador, pressão do coletor, combustível e sensores de O2).
- Documentação interativa OpenAPI/Swagger UI.

---

## 🏗️ Arquitetura do Projeto

```text
OBD2/
├── app/
│   ├── __init__.py
│   ├── main.py            # Instância FastAPI, documentação e healthcheck
│   ├── config.py          # Configurações e variáveis de ambiente
│   ├── schemas.py         # Schemas e validações com Pydantic v2
│   ├── database.py        # Camada de dados e repositórios
│   └── routes/
│       ├── auth.py        # Endpoints de autenticação de motoristas
│       ├── veiculos.py    # Listagem de veículos da frota
│       └── telemetria.py  # Ingestão de leituras OBD2
├── tests/
│   ├── test_health.py     # Testes de status e healthcheck
│   ├── test_auth.py       # Testes de validação de login e e-mail
│   ├── test_telemetria.py # Testes de payload de telemetria
│   └── test_cores.py      # Testes do utilitário de cores ANSI
├── Dockerfile             # Imagem de contêiner da aplicação
├── .dockerignore
├── requirements.txt       # Dependências da aplicação
├── coletaDadosOBD2.py     # Script legado de leitura OBD2
└── cores.py               # Utilitário de formatação de console
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório e criar ambiente virtual
```bash
git clone https://github.com/Lucas-Cayres-Porto/OBD2.git
cd OBD2
python -m venv .venv
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Rodar os testes
```bash
pytest -v
```

### 4. Iniciar o servidor FastAPI
```bash
uvicorn app.main:app --reload --port 8000
```
Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🐳 Executando via Docker

```bash
# Build da imagem Docker:
docker build -t obd2-api .

# Execução do contêiner:
docker run -p 8000:8000 obd2-api
```
