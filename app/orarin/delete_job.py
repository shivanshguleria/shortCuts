import app.danych.models as models
from fastapi import status, APIRouter, HTTPException, Depends
from app.danych.database import get_db
from sqlalchemy.orm import Session

from app.fief.firebase import delete_link
import app.danych.schemas as schemas


def del_link(uid: str, db):
    db.query(models.LinkProd).filter(models.LinkProd.unique_id == uid).update({"is_alive": False}, synchronize_session="fetch")
    delete_link(uid)
    db.commit()
    return True