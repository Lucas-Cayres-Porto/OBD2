# Imagem base oficial Python otimizada
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Instala ferramentas essenciais do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte da aplicação
COPY . .

# Expõe a porta 8000 utilizada pelo FastAPI
EXPOSE 8000

# Verificação de integridade do container (Healthcheck)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Comando padrão para inicializar o servidor de produção Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
