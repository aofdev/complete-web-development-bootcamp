from typing import Optional
from datetime import date
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

from entities.blog import Blog
from entities.book import Book
from repositories.blog import BlogRepository, BlogCreatePayload, BlogUpdatePayload
from repositories.book import BookRepository, NoBookError
from routes.book import book_router
from routes.blog import blog_router


app = FastAPI()
client = MongoClient("mongodb://cwdb101:!cwdb101!@localhost:27020")
blog_repo = BlogRepository(client["bootcamp"]["blogs"])
book_repo = BookRepository(client["bootcamp"]["books"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Complete Web Developer Bootcamp 2020"}


app.include_router(
    blog_router(blog_repo),
    prefix="/blogs",
    tags=["blogs"]
)

app.include_router(
    book_router(book_repo),
    prefix="/books",
    tags=["books"],
)
