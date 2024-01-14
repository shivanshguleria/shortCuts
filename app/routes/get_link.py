import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, Request, APIRouter
from urllib.parse import urlparse
from fastapi.responses import  RedirectResponse
from psycopg2.extras import RealDictCursor
from app.fief.firebase import update_count


import os

URI = os.getenv('DATABASE_URL')
result = urlparse(URI)


templates = Jinja2Templates(directory="templates")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

router = APIRouter()
TABLESTR="CREATE TABLE IF NOT EXISTS link_prod1 (id serial NOT NULL,unique_id varchar NOT NULL, link varchar NOT NULL, short_link varchar NOT NULL PRIMARY KEY,hex_code varchar DEFAULT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), is_preview BOOL DEFAULT false)"
@router.get('/{id}', response_class=RedirectResponse)
def get_link(id: str, request: Request):
    conn = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port,
        cursor_factory=RealDictCursor
    )
    cursor =  conn.cursor()
    cursor.execute(TABLESTR) # type: ignore
    print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
    cursor.execute("""SELECT link, is_preview FROM link_prod1 WHERE short_link = (%s);""",[id])
    post = cursor.fetchone()
    conn.close()
    if post == None:
    
        return templates.TemplateResponse("temp.html", {"request": request}, status_code=status.HTTP_404_NOT_FOUND)
    link = post['link'] # type: ignore
    update_count(id) # type: ignore
    if(link[0:5] != 'https'):
        link = "https://" + link + "/"
    if post['is_preview']: # type: ignore
        preview = link[0:40] + "\n..."

        return templates.TemplateResponse("preview.html", {"request": request, "link": link, "preview": preview})

    return link