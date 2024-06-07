# Dependency
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.danych.get_cred import Credentials # get credentials
# "postgresql://root:root@localhost/postgres"

engine = create_engine(
    Credentials.postgres
)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
        Returns  db instance from pool
    """
    db = SessionLocal()
    print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
    try:
        yield db
    finally:
        print("[INFO] Connection Closed")
        db.close()
