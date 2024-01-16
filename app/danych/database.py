from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy.schema as create


import os

URI = os.getenv('DATABASE_URL')
print(URI)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    URI
)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
    try:
        yield db
    finally:
        print("[INFO] Connection Closed")
        db.close()