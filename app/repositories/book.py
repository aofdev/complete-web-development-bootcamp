
from pymongo.collection import Collection
from entities.book import Book
from bson.objectid import ObjectId
from typing import Dict
from pprint import pprint


class BookRepository():
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_all(self):
        books = [self.map_raw_to_book(book_raw)
                 for book_raw in self.collection.find()]
        return books

    def find_by_id(self, book_id: str):
        book_raw = self.collection.find_one({"_id": ObjectId(book_id)})
        if (book_raw is None):
            raise NoBookError
        book = self.map_raw_to_book(book_raw)
        return book

    def create(self, book: Book):
        inserted_result = self.collection.insert_one(
            book.dict(exclude_unset=True))
        inserted_id = str(inserted_result.inserted_id)
        return inserted_id

    def update(self, book_id: str, book: Book):
        updated_result = self.collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": book.dict(exclude_unset=True)})
        if updated_result.modified_count == 0:
            raise NoBookUpdateError
        return book_id

    def delete(self, book_id: str):
        deleted_result = self.collection.delete_one({"_id": ObjectId(book_id)})
        if deleted_result.deleted_count == 0:
            raise NoBookDeleteError
        return book_id

    def map_raw_to_book(self, book_raw: Dict):
        return Book(**{
            "id": str(book_raw["_id"]) if "_id" in book_raw else None,
            "title": book_raw["title"] if "title" in book_raw else None,
            "isbn": book_raw["isbn"] if "isbn" in book_raw else None,
            "page_count": book_raw["page_count"] if "page_count" in book_raw else None,
            "published_date": book_raw["published_date"] if "published_date" in book_raw else None,
            "thumbnail_url": book_raw["thumbnail_url"] if "thumbnail_url" in book_raw else None,
            "short_description": book_raw["short_description"] if "short_description" in book_raw else None,
            "long_description": book_raw["long_description"] if "long_description" in book_raw else None,
            "status": book_raw["status"] if "status" in book_raw else None,
            "authors": book_raw["authors"] if "authors" in book_raw else None,
            "categories": book_raw["categories"] if "categories" in book_raw else None
        })


class NoBookError(Exception):
    """Raised when the no book is found from db"""
    pass


class NoBookUpdateError(Exception):
    """Raised when failed to update book in db"""
    pass


class NoBookDeleteError(Exception):
    """Raised when failed to delete book in db"""
    pass
