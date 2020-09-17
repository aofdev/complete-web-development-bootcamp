from pydantic import BaseModel
from datetime import datetime


class Blog(BaseModel):
    id: str
    title: str
    body: str
    author: str
    cover_image_url: str
    created_date: datetime
    last_edited_date: datetime
