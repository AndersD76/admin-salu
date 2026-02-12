from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load .env.production if it exists (for Railway/production)
if os.path.exists(".env.production"):
    load_dotenv(".env.production")
else:
    load_dotenv()


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Admin Salu - Painel Administrativo"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 dias

    # XML Feed (pode ser multiplas URLs separadas por virgula)
    XML_SOURCE_URL: str = ""
    XML_SOURCE_URLS: str = ""

    def get_xml_urls(self) -> List[str]:
        """Retorna lista de URLs de XML (suporta multiplas fontes)"""
        urls = []
        if self.XML_SOURCE_URL:
            urls.append(self.XML_SOURCE_URL.strip())
        if self.XML_SOURCE_URLS:
            for url in self.XML_SOURCE_URLS.split(','):
                url = url.strip()
                if url:
                    urls.append(url)
        return urls

    # Cron/Scheduler
    CRON_SECRET: str = ""

    # CORS (configure via env: ALLOWED_ORIGINS=["https://app.salu.com"])
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    model_config = {
        "case_sensitive": False,
        "extra": "ignore"
    }


settings = Settings()
