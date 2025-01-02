import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('app.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Vecinet"
    PROJECT_VERSION: str = "0.1"

    MYSQL_USER: str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@junction.proxy.rlwy.net:29763/railway"

settings = Settings()