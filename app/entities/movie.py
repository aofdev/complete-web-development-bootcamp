from typing import List, Optional
from pydantic import BaseModel


class Movie(BaseModel):
    id: Optional[str]
    name: Optional[str]
    genres: Optional[List[str]]
    poster: Optional[str]
    synopsis: Optional[str]
    release_date: Optional[str]
