import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from pathlib import Path
env_path = Path('app.') / '.env'
load_dotenv(dotenv_path=env_path)

# Obtaining db URL
MYSQL_URL = os.getenv("MYSQL_URL")

# Creating db engine
engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True
)

# Configurating db session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

# Function to manage db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#--------------------------------------
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)