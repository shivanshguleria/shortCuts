import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, APIRouter, HTTPException
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel

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

class Link_delete(BaseModel):
    shortLink: str
    token: str


@router.delete('/api/delete/', status_code=status.HTTP_204_NO_CONTENT)
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

