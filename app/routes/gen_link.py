import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, APIRouter, HTTPException
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor
from app.fief.firebase import  push_new_count

from pydantic import BaseModel
from typing import Optional
from app.fief.generater import generate_unique_id, genrate_random_string

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

TOKENDB = 'CREATE TABLE IF NOT EXISTS tokens (id serial NOT NULL, token varchar NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now())'
TABLESTR="CREATE TABLE IF NOT EXISTS link_prod1 (id serial NOT NULL,unique_id varchar NOT NULL, link varchar NOT NULL, short_link varchar NOT NULL PRIMARY KEY,hex_code varchar DEFAULT NULL, created_at timestamp with time zone NOT NULL DEFAULT now(), is_preview BOOL DEFAULT false)"


class Link(BaseModel):
    link: str
    customLink: Optional[str] = None
    is_preview: Optional[bool] = False
    token: Optional[str] = None

@router.post('/api/link', status_code=status.HTTP_201_CREATED)
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
