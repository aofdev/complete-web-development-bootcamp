from typing import Optional
from datetime import date

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from library import Library, Book, NoBookError
from pymongo import MongoClient
from bson.objectid import ObjectId
from payload import CreateBookIn, UpdateBookIn
import uuid


app = FastAPI()
library = Library()
client = MongoClient("mongodb://root:root@localhost:27017")
db = client.bootcamp


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books")
def read_books():
    blogs_raw = [blog_raw for blog_raw in db.blogs.find()]

    blogs = map(lambda br: {
        "id": str(br["_id"]),
        "title": br["title"],
        "author": br["author"],
        "published_date": br["published_date"].strftime("%d-%b-%Y (%H:%M:%S.%f)")
    }, blogs_raw)

    return {
        "message": "ok",
        "data": list(blogs)
    }


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: str, response: Response):
    # book = library.get_book_with_id(book_id)

    book_raw = db.blogs.find_one({"_id": ObjectId(book_id)})

    if book_raw is None:
        response.status_code = 500
        return {"message": "book not found"}

    book = {
        "id": str(book_raw["_id"]),
        "title": book_raw["title"],
        "author": book_raw["author"],
        "published_date": book_raw["published_date"].strftime("%d-%b-%Y (%H:%M:%S.%f)")
    }
    return {
        "message": "ok",
        "data": book
    }


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: CreateBookIn):
    new_book = library.create_book(book)
    return {
        "message": "ok",
        "data": new_book
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
