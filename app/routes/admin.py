from fastapi import status, APIRouter, HTTPException, Depends
from app.fief.firebase import delete_routine, get_count_reference, push_updated_data

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session
import app.danych.schemas as schemas

router = APIRouter()

@router.post('/api/admin/get')
def remove(req: schemas.Admin, db: Session = Depends(get_db)):
    if req.body == "7fc9e98537c470d55f995d45fa6e3bcaefb0020e831db5c43d3fda0b6888e90e77fa2b74867c8020a9e93797362ce794538c":
        
        get_short_link_in_db = db.query(models.LinkProd.short_link).all()
        get_firebase_count = delete_routine()
        new_dict = {}
        for i in range(len(get_short_link_in_db)):
            if get_firebase_count.get(get_short_link_in_db[i][0]) != None:
                new_dict[get_short_link_in_db[i][0]] =  get_firebase_count.get(get_short_link_in_db[i][0])
            get_count_reference()
            push_updated_data(new_dict)
        return {"message": "redundant links removed",
                "len_before": len(get_firebase_count),
                "len_after": len(new_dict),
                "diff":  len(get_firebase_count) - len(new_dict)
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth wrong")
