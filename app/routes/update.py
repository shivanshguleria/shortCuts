import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, APIRouter, HTTPException
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel
from typing import Optional

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

class Update(BaseModel):
    token: str
    unique_id: str
    link: Optional[str] = None
    short_link: Optional[str] = None
    is_preview: Optional[bool] = None

@router.put('/api/update/', status_code=status.HTTP_204_NO_CONTENT)
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
