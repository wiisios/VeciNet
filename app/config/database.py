import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from pathlib import Path
env_path = Path('app.') / '.env'
load_dotenv(dotenv_path=env_path)

MYSQL_URL = os.getenv("MYSQL_URL")

engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def createDbAndTables():
    SQLModel.metadata.create_all(engine)