from fastapi import status, APIRouter, HTTPException, Depends

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

import app.danych.schemas as schemas
from app.fief.validate import validate_link
router = APIRouter()

@router.put('/api/update/', status_code=status.HTTP_204_NO_CONTENT)
def update_link(req: schemas.Handle_Update, db: Session= Depends(get_db)):
    check_unique_id_and_token = db.query(models.LinkProd).filter(models.LinkProd.token == req.token and models.LinkProd.unique_id == req.unique_id).first()
    print(check_unique_id_and_token)
    if check_unique_id_and_token != None :
        if req.link and not req.short_link and not req.is_preview:
            if validate_link(req.link):
                db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update({"link": req.link}, synchronize_session="fetch")
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Enter Valid Link")
        elif req.short_link and not req.link and not req.is_preview:
            # check_short_link_in_db = db.query(models.LinkProd).filter(models.LinkProd.short_link == req.short_link).first()
            if not check_unique_id_and_token.short_link == req.short_link:
                db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update({"short_link": req.short_link}, synchronize_session="fetch")

            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post with short link exists")
        elif req.is_preview and not req.short_link and not req.link:

            # check_is_preview = db.query(models.LinkProd.is_preview).filter(models.LinkProd.unique_id == req.unique_id).first()

            if check_unique_id_and_token.is_preview == req.is_preview:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Link is already set to {req.is_preview}")
            else:
                db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update({"is_preview": req.is_preview}, synchronize_session="fetch")
        elif not req.is_preview and not req.short_link and not req.link:

            # check_is_preview = db.query(models.LinkProd.is_preview).filter(models.LinkProd.unique_id == req.unique_id).first()

            if check_unique_id_and_token.is_preview == req.is_preview:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Link is already set to {req.is_preview}")
            else:
                db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update({"is_preview": req.is_preview}, synchronize_session="fetch")
        else:

            # check = db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).first()
            if validate_link(req.link):
                if check_unique_id_and_token.short_link != req.short_link:
                    db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update({"is_preview": req.is_preview, "link": req.link, "short_link": req.short_link}, synchronize_session="fetch")
                else:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post with short link exists")
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Enter Valid Link")
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link \n or unique ID does not exist")
