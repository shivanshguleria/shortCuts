from pydantic import BaseModel
from typing import Optional

from datetime import datetime

class Link(BaseModel):
    link: str
    customLink: Optional[str] = None
    is_preview: Optional[bool] = False
    token: Optional[str] = None


class Handle_link_return(BaseModel):
    link: str
    short_link: str
    created_at: datetime
    is_preview: bool
    unique_id: str

class Handle_Update(BaseModel):
    token: str
    unique_id: str
    link: Optional[str] = None
    short_link: Optional[str] = None
    is_preview: Optional[bool] = None