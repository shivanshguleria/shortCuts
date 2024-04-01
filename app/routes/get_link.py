
from fastapi.templating import Jinja2Templates
from fastapi import status, Request, APIRouter, Depends
from fastapi.responses import  RedirectResponse

# from app.fief.firebase import update_count\
from app.danych.mongo import update_count

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

import app.danych.schemas as schemas

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get('/{id}', response_class=RedirectResponse)
def get_link(id: str, request: Request, db: Session= Depends(get_db)):
    link_store = db.query(models.LinkProd).filter(models.LinkProd.short_link == id).first()
    print(link_store)
    if link_store  and link_store.is_alive:
        if link_store.token:
            if(request.headers["cf-ipcountry"]):
                update_count(link_store.unique_id, request.headers["cf-ipcountry"])
        if link_store.is_preview:
            return templates.TemplateResponse("preview.html", {"request": request, "link": link_store.link, "preview": link_store.link[0:40] + "\n..."})
        else:
            return RedirectResponse(link_store.link)
    else:
        return templates.TemplateResponse("temp.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)
    
# 
@router.get('/api/get', status_code=status.HTTP_202_ACCEPTED) #, response_model=schemas.Get_all_count)
def get_all_links(token: str, db: Session= Depends(get_db)):
    get_all = db.query( models.LinkProd.link, models.LinkProd.short_link,  models.LinkProd.timestamp, models.LinkProd.is_preview,models.LinkProd.unique_id,).filter(models.LinkProd.token == token).all()
    return handle_link_return(get_all)


def handle_link_return(list_obj: list):
    return_list = list()
    for i in range(len(list_obj)):
        return_list.append(dict(zip(['link', 'short_link', 'timestamp', 'is_preview', 'unique_id'], list_obj[i])))
    return return_list


