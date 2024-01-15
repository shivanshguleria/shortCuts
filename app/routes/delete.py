from fastapi import status, APIRouter, HTTPException, Depends
from pydantic import BaseModel
import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class Link_delete(BaseModel):
    shortLink: str
    token: str

@router.delete('/api/delete/', status_code=status.HTTP_204_NO_CONTENT)
def delete_data(req: Link_delete, db: Session = Depends(get_db)):
    check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == req.token).first()
    if check_token_in_db:
        check_hex_code_relation = db.query(models.LinkProd.short_link).filter(models.LinkProd.short_link == req.shortLink).first()
        if check_hex_code_relation:
            delete_object = db.query(models.LinkProd).filter(models.LinkProd.short_link == req.shortLink).first()
            print(str(check_token_in_db), check_hex_code_relation, delete_object)
            db.delete(delete_object)
            db.commit()
            db.refresh()
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token does not exists")

