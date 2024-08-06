import app.danych.models as models
# from app.fief.firebase import delete_link
from app.danych.mongo import delete_link_upsert
from app.danych.database import SessionLocal

def del_link(uid: str):
    try:
        session = SessionLocal()
        session.query(models.LinkProd).filter(models.LinkProd.unique_id == uid).update({"is_alive": False}, synchronize_session="fetch")
        delete_link_upsert(uid)
        session.commit()
    finally:
        session.close()