from fastapi import APIRouter, Depends, status

from app.fief.generater import generate_token

import app.danych.models as models
import app.danych.schemas as schemas
from app.danych.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/token", response_model= schemas.Handle_token_return,status_code=status.HTTP_201_CREATED)
def generates(db: Session = Depends(get_db)):
    token_str = models.Tokens(token= generate_token())
    db.add(token_str)
    db.commit()
    return token_str
