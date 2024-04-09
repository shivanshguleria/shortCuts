from fastapi import status, APIRouter, Depends
# from app.fief.firebase import  get_count
from app.danych.mongo import get_count, find_unique_id

from fastapi import HTTPException

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session
from app.danych.schemas import Handle_count_return, Get_all_count

router = APIRouter()

@router.post("/api/count/all/{token}")
def get_all_count(req: Get_all_count,token:str, db:Session = Depends(get_db)):
    check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == token).first()
    if check_token_in_db and check_token_in_db.token == token:
        count_list = list()
        for i in range(len(req.links)):
            if find_unique_id(req.links[i]):
                count = get_count(req.links[i])
                count_list.append({"unique_id":req.links[i], "count": count["count"], "analytics": count["analytics"]})
            else:
                count_list.append(-1)
        return count_list
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token is not true")




@router.get("/api/count/{token}/{id}")
def count(id: str, token:str, db: Session = Depends(get_db)):
    check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == token).first()
    if check_token_in_db and check_token_in_db.token == token:
        check_unique_id = db.query(models.LinkProd.unique_id).filter(models.LinkProd.unique_id == id).first()
        print(check_unique_id)
        if check_unique_id != None and check_unique_id[0] == id:
            count = get_count(id)
            return  count
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Link does not exist")    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token is not true")

