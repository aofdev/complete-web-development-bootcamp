from typing import Optional
from datetime import date

from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from library import Library, Book, NoBookError
import uuid


app = FastAPI()
library = Library()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books")
def read_books():
    return {
        "message": "ok",
        "data": library.get_all_books()
    }


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int, response: Response):
    book = library.get_book_with_id(book_id)
    if book is None:
        response.status_code = 500
        return {"message": "book not found"}
    return {
        "message": "ok",
        "data": book
    }


class CreateBookIn(BaseModel):
    title: str
    author: str
    published_date: date


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book: CreateBookIn):
    new_book = library.create_book(book)
    return {
        "message": "ok",
        "data": new_book
    }


class UpdateBookIn(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_date: Optional[date]


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
