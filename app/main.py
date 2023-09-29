from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from .generater import genrate_random_string
import psycopg2,time
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

URI = os.getenv("DATABASEURL")


#Change link_prod during dev
while True:
    try:
        conn = psycopg2.connect(URI, sslmode="require", cursor_factory=RealDictCursor)
        cursor =  conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS link_prod (id serial NOT NULL, link varchar NOT NULL, short_link varchar PRIMARY KEY NOT NULL,count int NOT NULL DEFAULT 0, created_at timestamp with time zone NOT NULL DEFAULT now())")
        print("🗄️  🚀🚀")
        break
    except Exception as err:
        print(err)
        time.sleep(2)

class Link(BaseModel):
    link: str
    customLnk: Optional[str] = None

@app.get('/')
def root():
    return {"Hello": "World"}

@app.post('/link')
def add_link(req: Link):
    cursor.execute("INSERT INTO link_prod (link, short_link) VALUES (%s, %s) RETURNING *", (req.link, genrate_random_string()))
    post = cursor.fetchall()
    conn.commit()
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
    cursor.execute("""UPDATE link_prod SET count = count + 1 WHERE short_link = (%s)""", [id] )
    conn.commit()
    cursor.execute("""SELECT link FROM link_prod WHERE short_link = (%s);""",[id])
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    link = post['link'] # type: ignore
    if(link[0:5] != 'https'):
        link = "https://" + link + "/"
    return RedirectResponse(link)
    #return {"hello": "world"}
