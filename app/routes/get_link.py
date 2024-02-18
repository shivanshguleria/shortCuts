
from fastapi.templating import Jinja2Templates
from fastapi import status, Request, APIRouter, Depends
from fastapi.responses import  RedirectResponse

from app.fief.firebase import update_count

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get('/{id}', response_class=RedirectResponse)
def get_link(id: str, request: Request, db: Session= Depends(get_db)):
    link_store = db.query(models.LinkProd.link, models.LinkProd.is_preview).filter(models.LinkProd.short_link == id).first()
    if link_store:
        if(link_store.link[0:5] != 'https'):
            link = "https://" + link_store.link + "/"
        else:
            link = link_store.link
        check_token_relation = db.query(models.LinkProd).filter(models.LinkProd.short_link == id).first()
        if check_token_relation.token:
            update_count(check_token_relation.unique_id)
        if link_store.is_preview:
            return templates.TemplateResponse("preview.html", {"request": request, "link": link, "preview": link[0:40] + "\n..."})
        else:
            return RedirectResponse(link)
    else:
        return templates.TemplateResponse("temp.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)
    
# 
@router.get('/api/get', status_code=status.HTTP_202_ACCEPTED)
def get_all_links(token: str, db: Session= Depends(get_db)):
    
    get_all = db.query( models.LinkProd.link, models.LinkProd.short_link,  models.LinkProd.timestamp, models.LinkProd.is_preview,models.LinkProd.unique_id,).filter(models.LinkProd.token == token).all()
    print(get_all)
    return handle_link_return(get_all)


def handle_link_return(list_obj: list):
    return_list = list()
    for i in range(len(list_obj)):
        return_list.append(dict(zip(['link', 'short_link', 'timestamp', 'is_preview', 'unique_id'], list_obj[i])))
    return return_list


