
from fastapi import status, APIRouter, HTTPException, Depends
from app.fief.firebase import  push_new_count


from app.fief.generater import generate_unique_id, genrate_random_string

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session


# from app.crud.crud import get_token_in_db

import app.danych.schemas as schemas

router = APIRouter()



def return_type(post):
    return {
        "link": post.link,
        "short_link": post.short_link,
        "created_at": post.created_at,
        "is_preview": post.is_preview,
        "unique_id": post.unique_id
    }


@router.post('/api/link', status_code=status.HTTP_201_CREATED)
def add_link(req:schemas.Link, db: Session = Depends(get_db)):
    if req.token:
        check_token_in_db = db.query(models.Tokens).filter(models.Tokens.token == req.token).first()
        if check_token_in_db:
            if req.customLink != None:
                check_link_in_db = db.query(models.LinkProd.id).filter(models.LinkProd.short_link == req.customLink).first()
                if not check_link_in_db and req.customLink != "":
                    post = models.LinkProd(link= req.link, short_link= req.customLink, is_preview=req.is_preview, unique_id= generate_unique_id(), hex_code=req.token)
                    ref = req.customLink
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Custom code exists")
            else:
                ref = genrate_random_string()
                post = models.LinkProd(link= req.link, short_link= ref, is_preview=req.is_preview, unique_id= generate_unique_id(), hex_code=req.token) 
            push_new_count(ref)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tokens does not exists")
    else:
        ref = genrate_random_string()
        post = models.LinkProd(link= req.link, short_link= ref, is_preview=req.is_preview, unique_id= generate_unique_id(), hex_code=req.token)
    db.add(post)
    db.commit()
    return return_type(post)


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
