import token
from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from httplib2 import RETRIES
from pydantic import BaseModel
from typing import Optional
import app.danych.models as models
from app.danych.database import engine

from .routes import get_link, count, token, gen_link, delete, update, admin

from app.fief.schedule_delete import scheduler

models.Base.metadata.create_all(bind=engine)
scheduler.start()
# from sqlalchemy import Null, false, null
# from .get_ver import get_version


app = FastAPI(redoc_url=None, docs_url=None)

app.mount("/public/src", StaticFiles(directory="src"), name="src")

app.mount("/public/src/modules", StaticFiles(directory="./src/modules"), name="modules")


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods=["GET", "POST","OPTIONS"],
    allow_headers=["*"]
)
#Change link_prod during dev
# TABLESTR="CREATE TABLE IF NOT EXISTS link_prod1 (id serial NOT NULL,unique_id varchar NOT NULL, link varchar NOT NULL, short_link varchar NOT NULL PRIMARY KEY,hex_code varchar DEFAULT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), is_preview BOOL DEFAULT false)"
# TOKENDB = 'CREATE TABLE IF NOT EXISTS tokens (id serial NOT NULL, token varchar NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now())'
# URI = os.getenv('DATABASE_URL')
# KEYSTRING = os.getenv('KEY_STRING')

# # 'postgres://postgres:root@localhost/postgres'
# # 
# # result = urlparse('postgres://postgres:root@localhost/postgres')
# result = urlparse(URI)

# username = result.username
# password = result.password
# database = result.path[1:]
# hostname = result.hostname
# port = result.port

templates = Jinja2Templates(directory="templates")

@app.get('/favicon.ico')
async def favicon():
    pass

@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})
    #return {"Hello": "World"}

@app.get('/About', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "version": "1.0.3"})

@app.get('/User', response_class=HTMLResponse)
def user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.get('/Documentation', response_class=HTMLResponse)
def docs(request: Request):
    return templates.TemplateResponse("doc.html", {"request": request})

@app.get("/api")
def hello_world():
    return {"Hello": "World"}

@app.get("/video")
def serve_video():
    return FileResponse("/home/ubuntu/1080p/Station.Eleven.S01E06.1080p.English.Esub.MoviesMod.org.mkv")
app.include_router(admin.router)
app.include_router(get_link.router)
app.include_router(count.router)
app.include_router(token.router)
app.include_router(gen_link.router)
app.include_router(update.router)
app.include_router(delete.router)


# @app.get('/ads.txt', response_class=FileResponse)
# def ads_txt():
#     return "./utils/ads.txt"

# @app.get("/sitemap.xml", response_class=FileResponse)
# def sitemap_xml():
#     return "./utils/sitemap.xml"

# @app.get("/robots.txt", response_class=FileResponse)
# def robots_txt():
#     return "./utils/robots.txt"



