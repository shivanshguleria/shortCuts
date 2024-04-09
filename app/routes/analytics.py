#Code for analytics page 
from fastapi import APIRouter, Depends,HTTPException,status, Request

#Get Templating lib
from fastapi.templating import Jinja2Templates
#Get database session
import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

#get analytics data
from app.danych.mongo import get_count

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/analytics/{token}/{unique_id}", status_code=status.HTTP_200_OK)
def serve_analytics_page(req: Request, token: str, unique_id: str, db: Session = Depends(get_db)):
    link_info = db.query(models.LinkProd).filter(models.LinkProd.unique_id == unique_id, models.LinkProd.token == token).first()
    # print(link_info.id)
    if link_info:
        # print(get_count(link_info.unique_id)['analytics'])
        return templates.TemplateResponse("analytics.html", {"request": req, "analytics": {
            "short_link": link_info.short_link,
            "unique_id": link_info.unique_id,
              "link": link_info.link,
              "is_preview": link_info.is_preview,
              "toggle": {
                  "value": 1 if link_info.is_disabled  else 0,
                  "textContent": "Enable Link" if link_info.is_disabled  else "Disable Link" ,
                  "color": "toggle-link-green" if link_info.is_disabled  else "toggle-link"
              }
        }})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Link does not Exist")