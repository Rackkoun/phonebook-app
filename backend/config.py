# file backend/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field

ROOT_PATH = Path(__file__).resolve().parents[1]

ENV_FILE = ROOT_PATH / ".env"

if ENV_FILE.exists():
    load_dotenv(str(ENV_FILE))

class BackendConfig(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = 5432

    @computed_field
    @property
    def POSTGRES_DB_URL(self) -> PostgresDsn:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

backend_config = BackendConfig()
