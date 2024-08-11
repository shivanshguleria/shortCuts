
from fastapi import status, APIRouter, HTTPException, Depends
# from app.fief.firebase import  push_new_count
from app.danych.mongo import push_new_count
from app.fief.validate import validate_link

from app.fief.generater import generate_unique_id, genrate_random_string

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

from app.orarin.schedule_delete import add_new_job

# from app.crud.crud import get_token_in_db

import app.danych.schemas as schemas

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
router = APIRouter()


reserved_codes = ["esc", "analytics", "raw"]
@router.post('/api/link', status_code=status.HTTP_201_CREATED, response_model=schemas.Handle_link_return)
def add_link(req:schemas.Link, db: Session = Depends(get_db)):
    if id in reserved_codes:
        return JSONResponse(jsonable_encoder({"message": "This is a reserved page"}))
    if validate_link(req.link):
        ref = generate_unique_id()
        if req.token:
            check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == req.token).first()
            if check_token_in_db:
                if req.short_link != None:
                    check_link_in_db = db.query(models.LinkProd.id).filter(models.LinkProd.short_link == req.short_link).first()
                    if not check_link_in_db and req.short_link != "":
                        post = models.LinkProd(link= req.link, short_link= req.short_link, is_preview=req.is_preview, unique_id= ref, token=req.token)
                    else:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Custom code exists")
                else:
                    post = models.LinkProd(link= req.link, short_link= genrate_random_string(), is_preview=req.is_preview, unique_id= ref, token=req.token) 
                if req.schedule_delete:
                    if not add_new_job(ref, req.schedule_delete):
                        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Scheduled date supplied is smaller than current datetime")
                push_new_count(ref)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tokens does not exists")
        else:
            post = models.LinkProd(link= req.link, short_link= genrate_random_string(), is_preview=req.is_preview, unique_id= ref, token=req.token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"status": 401, "message": "Enter valid Link"})
    db.add(post)
    db.commit()
    return post


""" line 66

        if req.customLink != None:
            check_link_in_db = db.query(models.LinkProd.id).filter(models.LinkProd.short_link == req.customLink).first()
            if check_link_in_db == None and req.customLink != "":
                post = models.LinkProd(link= req.link, short_link= req.customLink, is_preview=req.is_preview, unique_id= generate_unique_id(), hex_code=req.token)
                ref = req.customLink
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Custom code exists")
        else:
            ref = genrate_random_string()
            post = models.LinkProd(link= req.link, short_link= ref, is_preview=req.is_preview, unique_id= generate_unique_id(), hex_code=req.token)

"""
