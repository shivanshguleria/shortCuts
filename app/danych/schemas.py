from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class Link(BaseModel):
    link: str
    short_link: Optional[str] = None
    is_preview: Optional[bool] = False
    token: Optional[str] = None
    schedule_delete: Optional[datetime] = None

class Admin(BaseModel):
    body: str

class Link_delete(BaseModel):
    unique_id: str
    token: str

class Handle_link_return(BaseModel):
    link: str
    short_link: str
    timestamp: int
    is_preview: bool
    unique_id: str

class Handle_Update(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    unique_id: str
    link: Optional[str] = None
    short_link: Optional[str] = None
    is_preview: Optional[bool] = None
class Handle_token_return(BaseModel):
    token: str
    timestamp: int

class Handle_count_return(BaseModel):
    count: int

class Handle_all(BaseModel):
    links: List[Handle_link_return]