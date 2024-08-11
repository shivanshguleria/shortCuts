
from fastapi.templating import Jinja2Templates
from fastapi import status, Request, APIRouter, Depends, HTTPException
from fastapi.responses import  RedirectResponse

# from app.fief.firebase import update_count\
from app.danych.mongo import update_count

import app.danych.models as models
from app.danych.database import get_db
from sqlalchemy.orm import Session

import app.danych.schemas as schemas

from starlette.background import BackgroundTask


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/{id}', response_class=RedirectResponse)
def get_link(id: str, request: Request, db: Session= Depends(get_db)):

    link_store = db.query(models.LinkProd).filter(models.LinkProd.short_link == id).first()
    if link_store  and link_store.is_alive and not  link_store.is_disabled:
        task = None
        if link_store.token:
            if(request.headers.get("cf-ipcountry")):
                task = BackgroundTask(update_count, unique_id = link_store.unique_id, country=request.headers.get("cf-ipcountry")) 
        if link_store.is_preview:
            return templates.TemplateResponse("preview.html", {"request": request, "link": link_store.link, "preview": link_store.link[0:40] + "\n..."}, background=task)
        else:
            return RedirectResponse(link_store.link, background=task)
    else:
        return templates.TemplateResponse("temp.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)
    
# 

@router.get('/raw/{id}', response_model=schemas.Handle_raw_link_return, status_code=status.HTTP_200_OK         )
def get_raw_response(id: str, request:Request, db: Session= Depends(get_db)):
    """
    @Desc: Function for return raw link for given {id}
    @Params: id - short link 
    @Return: A stringified json object containing link and status code (200)
    """
    link_store = db.query(models.LinkProd).filter(models.LinkProd.short_link == id).first()

    if link_store  and link_store.is_alive and not  link_store.is_disabled:
        if link_store.token and (request.headers.get("cf-ipcountry")):
            update_count(unique_id= link_store.unique_id, country=request.headers.get("cf-ipcountry"))
        return link_store                        
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"status": 401, "message": "Enter valid Link"})


@router.get('/api/get', status_code=status.HTTP_202_ACCEPTED) #, response_model=schemas.Get_all_count)    print(handle_link_return(link_store))
def get_all_links(token: str, db: Session= Depends(get_db)):
    get_all = db.query( models.LinkProd.link, models.LinkProd.short_link,  models.LinkProd.timestamp, models.LinkProd.is_preview,models.LinkProd.unique_id,).filter(models.LinkProd.token == token).all()
    return handle_link_return(get_all)


def handle_link_return(list_obj: list):
    return_list = list()
    for i in range(len(list_obj)):
        return_list.append(dict(zip(['link', 'short_link', 'timestamp', 'is_preview', 'unique_id'], list_obj[i])))
    return return_list


