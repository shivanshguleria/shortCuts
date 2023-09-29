from fastapi import FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from .generater import genrate_random_string
import psycopg2,time
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

URI = os.getenv("DATABASEURL")

while True:
    try:
        conn = psycopg2.connect(URI, sslmode="require", cursor_factory=RealDictCursor)
        cursor =  conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS links (id serial NOT NULL, link varchar NOT NULL, short_link varchar PRIMARY KEY NOT NULL, created_at timestamp with time zone NOT NULL DEFAULT now())")
        print("🗄️  🚀🚀")
        break
    except Exception as err:
        print(err)
        time.sleep(2)

class Link(BaseModel):
    link: str
    customLnk: str = None


@app.get('/')
def root():
    return {"Hello": "World"}

@app.post('/link')
def add_link(req: Link):
    cursor.execute("INSERT INTO links (link, short_link) VALUES (%s, %s) RETURNING *", (req.link, genrate_random_string()))
    post = cursor.fetchall()
    conn.commit()
    return {"message": post}

@app.get('/link/{id}')
def get_link(id: str):
    print(id)
    cursor.execute("""SELECT link FROM links WHERE short_link = (%s)""",[id])
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    return RedirectResponse(post["link"],status_code=status.HTTP_303_SEE_OTHER)
    #return {"hello": "world"}