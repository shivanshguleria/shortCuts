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

    if not req.link and not req.short_link and (req.is_preview == None ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Empty Request Sent")
    if check_unique_id_and_token != None :
        req_as_list = list(req)[2:]
        for i in range(len(req_as_list)):
            # Find if req has data
            if(req_as_list[i][1] == None):
                req_as_list[i] = 0
            else:
                # Vlaidate data if err raise exception
                match req_as_list[i][0]:
                    case "link":
                         if not validate_link(req_as_list[i][1]):
                            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Enter Valid Link")
                    case "shortlink":
                        check_short_link_in_db = db.query(models.LinkProd).filter(models.LinkProd.short_link == req.short_link).first()
                        if check_short_link_in_db or check_unique_id_and_token.short_link == req.short_link:
                            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post with short link exists")
                    case "is_preview":
                        if check_unique_id_and_token.is_preview == req_as_list[i][1]:
                            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Link is already set to {req.is_preview}")

        db.query(models.LinkProd).filter(models.LinkProd.unique_id == req.unique_id).update(dict([data for data in req_as_list if data !=0]), synchronize_session="fetch")
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link \n or unique ID does not exist")


