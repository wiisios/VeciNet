import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# MYSQL_URL = os.getenv("MYSQL_URL")
MYSQL_URL = "mysql+pymysql://root:yXCaPaWXkWZWIvYkssutCofjwqkBlzbK@autorack.proxy.rlwy.net:28455/railway"

engine = create_engine(
    MYSQL_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def createDbAndTables():
    SQLModel.metadata.create_all(engine)