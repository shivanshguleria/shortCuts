from fastapi import status, APIRouter, Depends
from app.fief.firebase import  get_count


from fastapi import HTTPException

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/api/count/{token}/{id}")
def count(id: str, token:str, db: Session = Depends(get_db)):
    check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == token).first()
    if check_token_in_db and check_token_in_db.token == token:
        check_unique_id = db.query(models.LinkProd.unique_id).filter(models.LinkProd.unique_id == id)
        if check_unique_id == id:
            post = db.query(models.LinkProd.short_link).filter(models.LinkProd.unique_id==id).first()
            return {"count": get_count(post[0])}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Link id supplied is not true")    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token is not true")
