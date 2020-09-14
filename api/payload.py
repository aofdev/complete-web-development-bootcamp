from pydantic import BaseModel
from typing import Optional
from datetime import date


class CreateBookIn(BaseModel):
    title: str
    author: str
    published_date: date


class UpdateBookIn(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[date]
