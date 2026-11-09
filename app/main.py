from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, veiculos, telemetria

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## API de Telemetria e Ingestão de Dados Veiculares OBD2 🚛

    Esta API foi desenvolvida para receber, validar e gerenciar leituras de sensores de veículos via protocolo OBD2.
    
    ### Funcionalidades:
    * **Autenticação**: Validação e login seguro de motoristas.
    * **Veículos**: Consulta de frota vinculada ao motorista.
    * **Telemetria**: Ingestão de dados de motor, RPM, temperaturas, sensores de O2 e níveis de combustível.
    * **Healthcheck**: Monitoramento contínuo para suporte ao pipeline de CI/CD.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS para permitir integração com dashboards e frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos roteadores da API
app.include_router(auth.router)
app.include_router(veiculos.router)
app.include_router(telemetria.router)


@app.get("/", tags=["Geral"])
def raiz():
    return {
        "sistema": settings.APP_NAME,
        "versao": settings.APP_VERSION,
        "status": "online",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Geral"])
def healthcheck():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
