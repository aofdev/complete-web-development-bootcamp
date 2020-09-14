from typing import Optional
from datetime import date
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

from library import Library, Book, NoBookError
from payload import UpdateBookIn
from blog import BlogRepository, Blog, BlogCreatePayload
import uuid


app = FastAPI()
library = Library()
client = MongoClient("mongodb://root:root@localhost:27017")
blog_repo = BlogRepository(client["bootcamp"]["blogs"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/blogs")
def read_books():
    blogs = blog_repo.find_all()
    return {
        "message": "ok",
        "data": blogs
    }


@app.get("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def read_book(blog_id: str, response: Response):
    blog = blog_repo.find_by_id(blog_id)
    return {
        "message": "ok",
        "data": blog
    }


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_book(blog: BlogCreatePayload):
    new_blog_id = blog_repo.create(blog)
    return {
        "message": "ok",
        "data": {
            "blog_id": new_blog_id
        }
    }


@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
def update_book(book_id: int, update_book_payload: UpdateBookIn, response: Response):
    try:
        edited_book = library.update_book(book_id, Book(
            id=book_id, **update_book_payload.dict()))
        return {
            "message": "ok",
            "data": edited_book
        }
    except NoBookError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"book {book_id} not found"
        }


@app.delete("/books/{book_id}")
def delete_book(book_id: int, response: Response):
    try:
        deleted_book = library.delete_book(book_id)
        return {
            "message": "ok",
            "data": deleted_book
        }
    except NoBookError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"book {book_id} not found"
        }
