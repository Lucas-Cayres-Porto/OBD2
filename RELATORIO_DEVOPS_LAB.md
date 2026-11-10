# 🚛 Relatório Técnico: Pipeline CI/CD com IA Generativa
**Disciplina / Laboratório**: LAB – DevOps – Pipeline CI/CD  
**Instituição**: Instituto J&F – Centro de Educação para os Negócios  
**Aluno / Autor**: Lucas Cayres Porto  
**Data**: Outubro / Novembro de 2026  
**Repositório do Projeto**: [https://github.com/Lucas-Cayres-Porto/OBD2](https://github.com/Lucas-Cayres-Porto/OBD2)  

---

## 1. Identificação do Projeto e Contexto

O projeto escolhido para esta atividade é o **OBD2 - Telemetria Veicular & API REST**, uma aplicação backend desenvolvida em **Python 3.11** utilizando o framework **FastAPI**, **Pydantic v2**, **SQLAlchemy** e conteinerizada com **Docker**.

### Objetivo da Aplicação
Capturar, validar e persistir fluxos de dados de telemetria automotiva via protocolo OBD2 para frotas de caminhões e veículos pesados, oferecendo:
- Autenticação e identificação de motoristas;
- Vinculação de veículos de frotas ativas;
- Ingestão contínua de parâmetros críticos do motor (RPM, temperatura, aceleração, pressão e sensores de oxigênio);
- Documentação OpenAPI/Swagger interativa (`/docs`) e endpoint de monitoramento de integridade (`/health`).

---

## 2. Arquitetura da Pipeline CI/CD

A automação foi concebida utilizando **GitHub Actions**, dividida em dois jobs essenciais e interdependentes com nomenclaturas diretas e padronizadas: **CI - Integracao Continua** e **CD - Deploy Continuo**.

```mermaid
flowchart TD
    subgraph Gatilhos ["Eventos GitHub"]
        PR["Pull Request -> main"]
        PUSH["Push -> main"]
    end

    subgraph CI ["Job: CI - Integracao Continua"]
        direction TB
        C1["Checkout"] --> C2["Configurar Python"]
        C2 --> C3["Instalar Dependencias"]
        C3 --> C4["Lint (Flake8)"]
        C4 --> C5["Testes Unitarios (Pytest)"]
        C5 --> C6["Build da Imagem Docker"]
    end

    subgraph CD ["Job: CD - Deploy Continuo"]
        direction TB
        cond{"Branch é main && Push?"}
        D1["Checkout"]
        D2["Configurar Docker"]
        D3["Normalizar Tag da Imagem"]
        D4["Login no GHCR"]
        D5["Build e Push da Imagem"]
        
        cond -- Sim --> D1 --> D2 --> D3 --> D4 --> D5
    end

    PR --> CI
    PUSH --> CI
    CI -- "needs: ci (Sucesso)" --> cond
    cond -- "Não (Apenas PR)" --> FimPR["CI Concluído (PR liberado para Merge)"]
```

### Arquivo da Pipeline: `.github/workflows/ci-cd.yml`

```yaml
name: Pipeline CI/CD

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  ci:
    name: CI - Integracao Continua
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Instalar Dependencias
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Lint (Flake8)
        run: |
          # Interrompe se houver erros criticos de sintaxe ou variaveis indefinidas
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          # Alertas de estilo gerais (sem interromper)
          flake8 . --count --exit-zero --max-complexity=15 --statistics

      - name: Testes Unitarios (Pytest)
        run: |
          pytest -v --tb=short

      - name: Build da Imagem Docker
        run: |
          docker build -t obd2-api:test .

  cd:
    name: CD - Deploy Continuo
    needs: ci
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    timeout-minutes: 15
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configurar Docker
        uses: docker/setup-buildx-action@v3

      - name: Normalizar Tag da Imagem
        id: image_meta
        run: |
          REPO_LOWER=$(echo "${{ github.repository }}" | tr '[:upper:]' '[:lower:]')
          echo "IMAGE_NAME=ghcr.io/${REPO_LOWER}" >> $GITHUB_OUTPUT

      - name: Login no GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build e Push da Imagem
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ steps.image_meta.outputs.IMAGE_NAME }}:latest
            ${{ steps.image_meta.outputs.IMAGE_NAME }}:${{ github.sha }}
```

---

## 3. Justificativa da Estratégia de Deployment (CD)

O roteiro do laboratório estabelece expressamente a possibilidade de utilizar **Docker quando o projeto utiliza contêineres** como estratégia de deployment e release:

1. **Adequação Tecnológica**:
   O projeto OBD2 possui um `Dockerfile` otimizado (`python:3.11-slim`), com healthcheck e servidor de produção Uvicorn. Aplicações de telemetria automotiva e IoT são concebidas para distribuição em nós de borda (edge), clusters Kubernetes ou servidores de alta performance, onde a **imagem de contêiner é o artefato final entregável**.

2. **Publicação Contínua no GitHub Container Registry (GHCR)**:
   A cada push na branch `main`, após o sucesso irrestrito dos testes de CI, o CD gera e publica a nova versão do contêiner em `ghcr.io/lucas-cayres-porto/obd2`. São geradas simultaneamente duas tags: `:latest` (versão estável de produção mais recente para consumo imediato) e `:${{ github.sha }}` (rastreabilidade e imutabilidade atrelada ao hash exato do commit). O processo é 100% autônomo e seguro, utilizando o `GITHUB_TOKEN` nativo com permissão `packages: write`, sem depender de credenciais externas ou serviços adicionais. Qualquer ambiente com Docker pode baixar e executar a versão mais recente em um único comando:
   ```bash
   docker pull ghcr.io/lucas-cayres-porto/obd2:latest
   docker run -d -p 8000:8000 ghcr.io/lucas-cayres-porto/obd2:latest
   ```

---

## 4. Registro do Processo de Desenvolvimento com IA Generativa

A construção da pipeline foi realizada em colaboração direta com a IA Generativa (Antigravity / Gemini), atuando como Arquiteto de Software e Engenheiro DevOps.

### Tabela de Interações Relevantes com a IA

| # | Prompt Utilizado | Resultado Obtido | Alteração / Decisão Realizada |
|---|------------------|------------------|-------------------------------|
| **1** | *"quero que primeiro você entenda o projeto para /plan como devemos criar isso e o que faz mais sentido para o meu projeto"* | Diagnóstico completo da aplicação FastAPI, suíte de testes e proposição da arquitetura de automação. | Estruturação dos estágios de CI (lint, testes automatizados e smoke test do Docker) e CD (empacotamento de contêiner no GHCR). |
| **2** | *"sem o render, pode retirar"* | Eliminação de dependências externas de infraestrutura e simplificação da arquitetura de release. | Foco exclusivo do CD na publicação de contêineres versionados no GitHub Container Registry via GITHUB_TOKEN nativo. |
| **3** | *"certo, deixe os nomes simples dos processos tbm"* | Otimização da legibilidade visual de toda a pipeline na interface web do GitHub Actions. | Padronização com nomes objetivos para cada etapa: `Checkout`, `Configurar Python`, `Testes Unitarios`, `Login no GHCR`, entre outros. |

---

## 5. Respostas às Questões Obrigatórias do LAB

### 1. Quantos prompts foram necessários para chegar à versão final?
Foram necessários 3 prompts no total. No primeiro, pedi ajuda para a inteligência artificial entender o projeto e montar o plano inicial; no segundo, pedi para simplificar o processo e retirar ferramentas externas; e no terceiro, pedi para organizar e deixar os nomes de cada etapa bem simples e fáceis de entender.

### 2. Quais foram os principais problemas encontrados?
O primeiro problema foi que o GitHub não aceitava letras maiúsculas na hora de registrar a versão do projeto, então foi preciso fazer um ajuste para converter tudo em letras minúsculas automaticamente. Além disso, o código do projeto mostrava alguns avisos antigos de configuração que precisavam ser atualizados para não atrapalhar a execução.

### 3. Quais alterações foram necessárias?
Foi preciso criar o arquivo que ensina o GitHub a fazer os testes e a publicação sozinho, além de um arquivo com regras para conferir se o código estava bem escrito. Também fizemos uma pequena correção no código do projeto para modernizar uma configuração antiga e adicionamos um resumo explicativo no projeto.

### 4. Quais alterações foram realizadas manualmente?
As únicas ações manuais foram escolher o repositório, avaliar as sugestões da IA, enviar os arquivos pelo computador e abrir uma proposta de alteração através da Pull Request #1 (https://github.com/Lucas-Cayres-Porto/OBD2/pull/1) para testar o fluxo antes de juntar tudo na versão definitiva.

### 5. Como você verificou que a pipeline estava funcionando corretamente?
Primeiro, testei o projeto no meu próprio computador para ter certeza de que tudo funcionava. Depois, abri a Pull Request #1 (https://github.com/Lucas-Cayres-Porto/OBD2/pull/1) no GitHub para conferir se a automação fazia todos os testes sozinha antes de aceitar a mudança. Por fim, ao aprovar e juntar na versão principal, vi pela tela do GitHub que todas as etapas passaram com sucesso, ficando com o símbolo verde de aprovação e gerando a versão final do sistema.

---

## 6. Evidências de Execução

> [!TIP]
> **Orientações para o envio do PDF:**
> Cole abaixo as capturas de tela do seu repositório no GitHub para comprovar a execução bem-sucedida da pipeline antes de gerar o PDF final:
> 1. Print da aba **Actions** mostrando os jobs de CI e CD verdes (✅): https://github.com/Lucas-Cayres-Porto/OBD2/actions/runs/42641244542
> 2. Print do **Pull Request #1** mostrando os testes aprovados antes do merge: https://github.com/Lucas-Cayres-Porto/OBD2/pull/1
> 3. Print da página de **Packages** no GitHub com o contêiner publicado: https://github.com/users/Lucas-Cayres-Porto/packages

### Comando para Testar a Imagem Publicada pelo CD:
```bash
# Baixar a versão mais recente publicada pela pipeline:
docker pull ghcr.io/lucas-cayres-porto/obd2:latest

# Executar o contêiner:
docker run -p 8000:8000 ghcr.io/lucas-cayres-porto/obd2:latest

# Testar healthcheck no navegador ou terminal:
curl http://localhost:8000/health
```
