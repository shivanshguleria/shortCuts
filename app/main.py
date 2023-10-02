from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .generater import genrate_random_string
import psycopg2,time
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()
app = FastAPI()

app.mount("/public/src", StaticFiles(directory="src"), name="src")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods=["GET", "POST","OPTIONS"],
    allow_headers=["*"]
)
#Change link_prod during dev
URI = os.getenv('DATABASEURL')

result = urlparse(URI)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

templates = Jinja2Templates(directory="templates")

#Change link_prod during dev
class Link(BaseModel):
    link: str
    customLnk: Optional[str] = None

@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    #return {"Hello": "World"}

@app.post('/link')
def add_link(req: Link):
    while True:
        try:
            conn = psycopg2.connect(
                database = database,
                user = username,
                password = password,
                host = hostname,
                port = port,
                cursor_factory=RealDictCursor
            )
            #conn = psycopg2.connect(URI, cursor_factory=RealDictCursor)
            cursor =  conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS link_prod (id serial NOT NULL, link varchar NOT NULL, short_link varchar PRIMARY KEY NOT NULL,count int NOT NULL DEFAULT 0, created_at timestamp with time zone NOT NULL DEFAULT now())")
            print("🗄️  🚀🚀")
            break
        except KeyboardInterrupt or Exception as err:
            print(err)
            time.sleep(2)
    cursor.execute("INSERT INTO link_prod (link, short_link) VALUES (%s, %s) RETURNING *", (req.link, genrate_random_string()))
    post = cursor.fetchall()
    conn.commit()
    conn.close()
    return {"message": post}

# @app.get("/{id}")
# def get_shrinked_link(id:str):
#     cursor.execute("""SELECT link FROM links WHERE short_link = (%s)""", [id])
#     post = cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {{id}} does not exists")
#     return RedirectResponse(post['link'])

@app.get('/{id}')
def get_link(id: str):
    while True:
        try:
            conn = psycopg2.connect(
                database = database,
                user = username,
                password = password,
                host = hostname,
                port = port,
                cursor_factory=RealDictCursor
            )
            cursor =  conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS link_prod (id serial NOT NULL, link varchar NOT NULL, short_link varchar PRIMARY KEY NOT NULL,count int NOT NULL DEFAULT 0, created_at timestamp with time zone NOT NULL DEFAULT now())")
            print("🗄️  🚀🚀")
            break
        except Exception as err:
            print(err)
            time.sleep(2)
    cursor.execute("""UPDATE link_prod SET count = count + 1 WHERE short_link = (%s)""", [id] )
    conn.commit()
    cursor.execute("""SELECT link FROM link_prod WHERE short_link = (%s);""",[id])
    post = cursor.fetchone()
    conn.close()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    link = post['link'] # type: ignore
    if(link[0:5] != 'https'):
        link = "https://" + link + "/"
    return RedirectResponse(link)
    #return {"hello": "world"}
