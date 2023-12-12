from sys import modules
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

from sqlalchemy import Null, false, null
from .get_ver import get_version
from .generater import genrate_random_string, generate_token, generate_unique_id
import psycopg2,time,re
from psycopg2.extras import RealDictCursor
from .firebase import delete_routine, get_count_reference , get_count_reference, push_updated_data, push_new_count, update_count, get_count

import os
from urllib.parse import urlparse

app = FastAPI(redoc_url="/Documentation", docs_url=None)

app.mount("/public/src", StaticFiles(directory="src"), name="src")

app.mount("/public/src/modules", StaticFiles(directory="./src/modules"), name="modules")


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods=["GET", "POST","OPTIONS"],
    allow_headers=["*"]
)
#Change link_prod during dev
TABLESTR="CREATE TABLE IF NOT EXISTS link_prod1 (id serial NOT NULL,unique_id varchar NOT NULL, link varchar NOT NULL, short_link varchar NOT NULL PRIMARY KEY,hex_code varchar DEFAULT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), is_preview BOOL DEFAULT false)"
TOKENDB = 'CREATE TABLE IF NOT EXISTS tokens (id serial NOT NULL, token varchar NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now())'
URI = os.getenv('DATABASE_URL')
KEYSTRING = os.getenv('KEY_STRING')

# 'postgres://postgres:root@localhost/postgres'
# 
# result = urlparse('postgres://postgres:root@localhost/postgres')
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
    customLink: Optional[str] = None
    is_preview: Optional[bool] = False
    token: Optional[str] = None
@app.get('/favicon.ico')
async def favicon():
    pass

@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})
    #return {"Hello": "World"}

@app.get('/About', response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "version": get_version()})

@app.get('/User', response_class=HTMLResponse)
def user(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "version": get_version()})


@app.get('/ads.txt', response_class=FileResponse)
def ads_txt():
    return "./utils/ads.txt"

@app.get("/sitemap.xml", response_class=FileResponse)
def sitemap_xml():
    return "./utils/sitemap.xml"

@app.get("/robots.txt", response_class=FileResponse)
def robots_txt():
    return "./utils/robots.txt"
@app.get('/{id}', response_class=RedirectResponse)
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
    # return {"shortLink": link}
    #return {"hello": "world"}
class Token(BaseModel):
    token: str

@app.get("/api/count/{token}/{id}")
def count(id: str, token:str):
    conn = psycopg2.connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port,
        cursor_factory=RealDictCursor
    )
    cursor =  conn.cursor()
    # print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
    # cursor.execute("""SELECT count FROM link_prod WHERE short_link = (%s) ;""",[id])
    # post = cursor.fetchall()
    # conn.close()
    cursor.execute("select token from tokens where token = (%s)", [token])
    auth_token = cursor.fetchone()
    if auth_token:
        if token == auth_token['token']: # type: ignore
            return { "count": get_count(id)}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token not supplied")
@app.get("/api/token")
def generate():
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
    cursor.execute(TOKENDB)
    cursor.execute("INSERT INTO tokens (token) VALUES (%s) RETURNING token, created_at", [generate_token()])
    post = cursor.fetchone()
    conn.commit()
    cursor.close()
    post['message'] = "Keep it somewhere safe!!" # type: ignore
    return post

@app.post('/api/link', status_code=status.HTTP_201_CREATED)
def add_link(req: Link):
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
    print(req)
    cursor.execute(TABLESTR)
    cursor.execute(TOKENDB) # type: ignore
    print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
    if req.token:
        cursor.execute("SELECT id from tokens where token = (%s)",[req.token])
        token_check = cursor.fetchone()
        if token_check:
            if req.customLink != None:
                cursor.execute('select id from link_prod1 where short_link = (%s);', [req.customLink])
                check = cursor.fetchone()
                if check == None and req.customLink != "":
                    cursor.execute("INSERT INTO link_prod1 (link, short_link, is_preview, hex_code, unique_id) VALUES (%s, %s, %s, %s, %s) RETURNING link, short_link,created_at, is_preview, unique_id", (req.link, req.customLink, req.is_preview, req.token, generate_unique_id()))
                    push_new_count(req.customLink)
                else:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Custom code exists")   
            else:
                short_link = genrate_random_string()
                cursor.execute("INSERT INTO link_prod1 (link, short_link, is_preview, hex_code, unique_id) VALUES (%s, %s, %s, %s, %s) RETURNING link, short_link,created_at, is_preview, unique_id", (req.link, short_link, req.is_preview, req.token, generate_unique_id()))
                push_new_count(short_link)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tokens does not exists")
    else:
        if req.customLink != None:
            cursor.execute('select id from link_prod1 where short_link = (%s);', [req.customLink])
            check = cursor.fetchone()
            if check == None and req.customLink != "":
                cursor.execute("INSERT INTO link_prod1 (link, short_link, is_preview, hex_code, unique_id) VALUES (%s, %s, %s, %s, %s) RETURNING link, short_link,created_at, is_preview, unique_id", (req.link, req.customLink, req.is_preview, req.token, generate_unique_id()))
                push_new_count(req.customLink)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Custom code exists")   
        else:
            short_link = genrate_random_string()
            cursor.execute("INSERT INTO link_prod1 (link, short_link, is_preview, hex_code, unique_id) VALUES (%s, %s, %s, %s, %s) RETURNING link, short_link,created_at, is_preview, hex_code, unique_id", (req.link, short_link, req.is_preview, req.token, generate_unique_id()))
            push_new_count(short_link)
    post = cursor.fetchone()
    # for i in post:
    #     for j in i:
    #       print(j,i[j])
    conn.commit()
    conn.close()
    return {"message": post}


class Del(BaseModel):
    body: str

class Link_delete(BaseModel):
    shortLink: str
    token: str


@app.delete('/api/delete/', status_code=status.HTTP_204_NO_CONTENT)
def delete_data(req: Link_delete):
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
    cursor.execute("SELECT * FROM tokens WHERE token = (%s)", [req.token])
    token_check_in_db = cursor.fetchone()
    if token_check_in_db:
        cursor.execute("SELECT hex_code FROM link_prod1 where short_link = (%s)", [req.shortLink])
        check_token_relation = cursor.fetchone()
        if check_token_relation:
            cursor.execute("DELETE FROM link_prod1 where short_link = (%s) returning short_link", [req.shortLink])
            conn.commit()
            cursor.close()
            
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token does not exists")


class Update(BaseModel):
    token: str
    unique_id: str
    link: Optional[str] = None
    short_link: Optional[str] = None
    is_preview: Optional[bool] = None

@app.put('/api/update/', status_code=status.HTTP_204_NO_CONTENT)
def update_links(req: Update):
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
    cursor.execute("SELECT * FROM link_prod1 WHERE hex_code = (%s) AND unique_id = (%s)", [req.token, req.unique_id])
    post = cursor.fetchone()
    print(bool(post))
    if post:
        if req.link and not req.short_link and not req.is_preview:
            cursor.execute("UPDATE link_prod1 set link = (%s) where unique_id = (%s)", [req.link, req.unique_id])
        elif req.short_link and not req.link and not req.is_preview:
            cursor.execute("SELECT * FROM link_prod1 WHERE short_link = (%s)", [req.short_link])
            check = cursor.fetchone()
            print(check)
            if not check:
                cursor.execute("UPDATE link_prod1 set short_link = (%s) where unique_id = (%s)", [req.short_link, req.unique_id])
                
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post with short link exists")
        elif req.is_preview or not req.short_link and not req.link:
            print(bool(req), req)
            cursor.execute("SELECT is_preview FROM link_prod1 WHERE unique_id = (%s)", [req.unique_id])
            check = cursor.fetchone()

            if check['is_preview'] == req.is_preview: # type: ignore
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Link is already set to {req.is_preview}")
            else:
                cursor.execute("UPDATE link_prod1 set is_preview = (%s) where unique_id = (%s)", [req.is_preview, req.unique_id])
        else:
            print(bool(req.link), req)
            cursor.execute("SELECT * FROM link_prod1 WHERE short_link = (%s)", [req.short_link])
            check = cursor.fetchone()
            print(check)
            if not check:
                cursor.execute("UPDATE link_prod1 set link = (%s), short_link = (%s), is_preview = (%s) where unique_id = (%s)", [req.link, req.short_link, req.is_preview, req.unique_id])
                
            else:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post with short link exists")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not related with short link \n or unique ID does not exist")
    conn.commit()
    conn.close()

# @app.post('/api/admin/get')
def remove(req: Del):
    if req.body == "7fc9e98537c470d55f995d45fa6e3bcaefb0020e831db5c43d3fda0b6888e90e77fa2b74867c8020a9e93797362ce794538c":
        
        conn = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname,
            port = port,
            cursor_factory=RealDictCursor
        )
        cursor =  conn.cursor()
        cursor.execute("SELECT short_link from link_prod1;")
        post = cursor.fetchall()
        cursor.execute("SELECT count(id) from link_prod1;")
        coun = cursor.fetchone()
        count_data = delete_routine()
        new_dict = {}
        for i in range(len(post)):
            if count_data.get(post[i]['short_link']) != null: # type: ignore
                new_dict[post[i]['short_link']] = count_data.get(post[i]['short_link']) # type: ignore
        get_count_reference()
        push_updated_data(new_dict)
        return {"message": "Redundant Links were removed",
                "link_count": coun,
                "Count": difference(len(post), len(count_data))}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth wrong")  

def difference(a, b):
    if(a > b):
        return a - b
    elif a < b:
        return b - a
    elif a == b:
        return 0
    else:
        return "error"
# @app.post('/link')
# def add_link(req: Link):
#     conn = psycopg2.connect(
#         database = database,
#         user = username,
#         password = password,
#         host = hostname,
#         port = port,
#         cursor_factory=RealDictCursor
#     )
#     cursor =  conn.cursor()
#     cursor.execute(table_str)
#     print("[INFO] 🗄️  🚀🚀 Postgres DB connected")
#     cursor.execute("INSERT INTO link_prod (link, short_link, is_preview) VALUES (%s, %s, %s) RETURNING link, short_link,created_at, is_preview", (req.link, genrate_random_string(), req.is_preview))
#     post = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return {"message": post}



# [RealDictRow(
#     [('id', 16),
#       ('link', 'prodserverme'),
#       ('short_link', 'bkoem'),
#       ('count', 0),
#       ('created_at', datetime.datetime(2023, 11, 5, 10, 34, 58, 809157, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800)))),
#       ('is_preview', True)
#       ]
#       )
# ]





