from fastapi import status, APIRouter, HTTPException, Depends
from pydantic import BaseModel
import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

from app.fief.firebase import delete_link
import app.danych.schemas as schemas

router = APIRouter()


@router.delete('/api/delete/', status_code=status.HTTP_204_NO_CONTENT)
def delete_data(req: schemas.Link_delete, db: Session = Depends(get_db)):
    check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == req.token).first()
    if check_token_in_db:
        check_hex_code_relation = db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).first()
        if check_hex_code_relation:
            delete_object = db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).first()
            db.delete(delete_object)
            db.commit()
            delete_link(delete_object.unique_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token does not exists")

