from fastapi import APIRouter, HTTPException, status, Depends

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session
from app.danych.schemas import toggle_link

router = APIRouter()

@router.put("/api/toggle/", status_code=status.HTTP_202_ACCEPTED)
def toggle(req:toggle_link, db: Session=Depends(get_db)):
    check_unique_id_and_token = db.query(models.LinkProd).filter(models.LinkProd.token == req.token and models.LinkProd.unique_id == req.unique_id).first()
    if(check_unique_id_and_token != None):
        db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id, models.LinkProd.token==req.token).update({"is_disabled": not check_unique_id_and_token.is_disabled}, synchronize_session="fetch")
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Link Does not exists")