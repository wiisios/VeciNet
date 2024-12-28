import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Vecinet"
    PROJECT_VERSION: str = "0.1"

    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@autorack.proxy.rlwy.net:28455/railway"

settings = Settings()