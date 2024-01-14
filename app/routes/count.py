import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, APIRouter
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor
from app.fief.firebase import  get_count


from fastapi import HTTPException


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

@router.get("/api/count/{token}/{id}")
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
            cursor.execute("select short_link from link_prod1 where unique_id = (%s)", [id])
            ref = cursor.fetchone()
            return { "count": get_count(ref['short_link'])}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token not supplied")