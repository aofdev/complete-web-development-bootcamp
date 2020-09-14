from pydantic import BaseModel
from datetime import date


class Blog(BaseModel):
    title: str
    body: str
    author: str
    category: str
    created_date: date
    last_edited_date: date
