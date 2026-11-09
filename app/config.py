import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "OBD2 Telemetria API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # Configurações do Banco de Dados PostgreSQL (preservando nomes do projeto original)
    HOSTTEST: str = os.getenv("HOSTTEST", "localhost")
    PORTTEST: int = int(os.getenv("PORTTEST", "5432"))
    DATABASETEST: str = os.getenv("DATABASETEST", "obd2_telemetria")
    USER: str = os.getenv("USER", "postgres")
    PASSWORDTEST: str = os.getenv("PASSWORDTEST", "postgres")

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.USER}:{self.PASSWORDTEST}@{self.HOSTTEST}:{self.PORTTEST}/{self.DATABASETEST}"



settings = Settings()
