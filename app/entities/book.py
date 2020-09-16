from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class Book(BaseModel):
    _id: Optional[int]
    title: Optional[str]
    isbn: Optional[str]
    page_count: Optional[int]
    published_date: Optional[datetime]
    thumbnail_url: Optional[str]
    short_description: Optional[str]
    long_description: Optional[str]
    status: Optional[str]
    authors: Optional[List[str]]
    categories: Optional[List[str]]
