import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor

from app.fief.generater import generate_token

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


@router.get("/api/token")
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