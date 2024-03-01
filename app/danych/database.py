from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# "postgresql://root:root@localhost/postgres"

engine = create_engine(
    "postgresql://root:root@localhost/postgres"
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
