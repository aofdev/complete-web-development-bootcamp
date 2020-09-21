
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Dict, List
from entities.book import Book
from bson import ObjectId
import asyncio


class AsyncBookRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection: AsyncIOMotorCollection = collection

    async def find_all(self) -> List[Book]:
        books = []
        async for book_raw in self.collection.find():
            book = self.map_raw_to_book(book_raw)
            books.append(book)
        return books

    async def find_by_id(self, id: str) -> Book:
        book_raw = await self.collection.find_one({"_id": ObjectId(id)})
        if book_raw is None:
            raise NoBookError
        return self.map_raw_to_book(book_raw)

    async def create(self, book: Book) -> str:
        inserted_result = await self.collection.insert_one(book.dict(exclude_unset=True))
        inserted_id = str(inserted_result.inserted_id)
        return inserted_id

    async def update(self, book_id: str, book: Book) -> str:
        updated_result = await self.collection.update_one({
            "_id": ObjectId(book_id)
        }, {
            "$set": book.dict(exclude_unset=True)
        })
        if updated_result.modified_count == 0:
            raise NoBookUpdateError
        return book_id

    async def delete(self, book_id: str) -> str:
        deleted_result = await self.collection.delete_one({"_id": ObjectId(book_id)})
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
    pass


class NoBookUpdateError(Exception):
    pass


class NoBookDeleteError(Exception):
    pass
