# file backend/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

ROOT_PATH = Path(__file__).resolve().parents[1]

ENV_FILE = ROOT_PATH / ".env"

if ENV_FILE.exists():
    load_dotenv(str(ENV_FILE))

class BackendConfig(BaseSettings):
    
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: int = int(os.getenv("DB_PORT"))

    @property
    def POSTGRES_DB_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

backend_config = BackendConfig()
