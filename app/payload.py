from pydantic import BaseModel
from typing import Optional
from datetime import date


class UpdateBookIn(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[date]
