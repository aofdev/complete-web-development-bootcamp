from datetime import date
from pydantic import BaseModel
from typing import Optional
import uuid


class Book(BaseModel):
    id: Optional[int] = 0
    title: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[date] = None


class Library():
    def __init__(self):
        books_raw = [
            {
                "id": 1,
                "title": "The principle",
                "author": "Ray Dalio",
                "published_date": date.today()
            },
            {
                "id": 2,
                "title": "7 Habits of highly effective people",
                "author": "Stephen R. Covey",
                "published_date": date.today()
            },
            {
                "id": 3,
                "title": "How to win friends and influence people",
                "author": "Dale Carnegie",
                "published_date": date.today()
            }
        ]

        self.books = [Book(**book_raw) for book_raw in books_raw]

    def get_all_books(self):
        return self.books

    def get_book_with_id(self, id: int):
        for book in self.books:
            if (book.id == id):
                return book
        return None

    def create_book(self, book: Book):
        new_book_id = uuid.uuid1().int >> 64
        new_book = Book(id=new_book_id, **book.dict())
        self.books.append(new_book)
        return new_book

    def update_book(self, book_id: int, book_payload: Book):
        book = self.get_book_with_id(book_id)
        if (book is None):
            raise NoBookError

        books = []
        for (index, b) in enumerate(self.books):
            if (b.id == book_id):
                to_be_updated_book_dict = b.dict()
                book_payload_dict = book_payload.dict()
                updated_book_dict = {**to_be_updated_book_dict}
                for key in book_payload_dict:
                    if (book_payload_dict[key] is not None):
                        updated_book_dict[key] = book_payload_dict[key]
                books.append(Book(**updated_book_dict))
            else:
                books.append(b)
        self.books = books
        return book

    def delete_book(self, book_id: int):
        book = self.get_book_with_id(book_id)
        if (book is None):
            raise NoBookError
        self.books = [book for book in self.books if book.id != book_id]
        return book


class NoBookError(Exception):
    """Raised when the no book is found"""
    pass
