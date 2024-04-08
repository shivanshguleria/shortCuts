from sqlalchemy import Boolean, Column, Sequence,func, Integer, String, func

from .database import Base


TOKENDB = '''CREATE TABLE IF NOT EXISTS tokens (
    id serial NOT NULL, 
    token varchar NOT NULL, 
    created_at timestamp with time zone NOT NULL DEFAULT now())'''
TABLESTR='''CREATE TABLE IF NOT EXISTS link_prod1 (
    id serial NOT NULL,
    unique_id varchar NOT NULL, 
    link varchar NOT NULL, 
    short_link varchar NOT NULL PRIMARY KEY,
    hex_code varchar DEFAULT NULL, 
    created_at timestamp with time zone NOT NULL DEFAULT now(), 
    is_preview BOOL DEFAULT false)'''

class LinkProd(Base):
    __tablename__ = "link_prod1"
    id = Column(Integer, Sequence("id_seq", start=1))
    unique_id = Column(String, unique=True)
    link = Column(String)
    short_link = Column(String, primary_key=True)
    token = Column(String, default=None)
    timestamp  = Column(Integer, default=func.extract('epoch' , func.now()))
    is_preview = Column(Boolean, default=False)
    is_alive=Column(Boolean, default=True)
    is_disabled = Column(Boolean, default=False)


class Tokens(Base):
    __tablename__ = "tokens"

    id = Column(Integer, Sequence("id_seq_token", start=1))
    token = Column(String, primary_key=True)
    timestamp = Column(Integer, default=func.extract('epoch' , func.now()))


