from fastapi import APIRouter, Depends

from app.fief.generater import generate_token

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/token")
def generates(db: Session = Depends(get_db)):
    token_str = models.Tokens(token= generate_token())
    db.add(token_str)
    db.commit()
    return {"token": token_str.token,
            "created_at": token_str.created_at,
            "message": "Keep it somewhere safe!!"
    }
