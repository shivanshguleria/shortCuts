import psycopg2 
from fastapi.templating import Jinja2Templates
from fastapi import status, APIRouter, HTTPException
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor
from app.fief.firebase import delete_routine, get_count_reference, push_updated_data

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

class Del(BaseModel):
    body: str

@router.post('/api/admin/get')
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