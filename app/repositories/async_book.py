
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Dict, List
from entities.book import Book
from bson import ObjectId
import asyncio


class AsyncBookRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection: AsyncIOMotorCollection = collection

    async def find_all(self) -> List[Book]:
        return [self.map_raw_to_book(book_raw) async for book_raw in self.collection.find()]

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
            "id": str(self.is_key_in_dict(key="_id", book_raw=book_raw)),
            "title": self.is_key_in_dict(key="title", book_raw=book_raw),
            "isbn": self.is_key_in_dict(key="isbn", book_raw=book_raw),
            "page_count": self.is_key_in_dict(key="page_count", book_raw=book_raw),
            "published_date": self.is_key_in_dict(key="published_date", book_raw=book_raw),
            "thumbnail_url": self.is_key_in_dict(key="thumbnail_url", book_raw=book_raw),
            "short_description": self.is_key_in_dict(key="short_description", book_raw=book_raw),
            "long_description": self.is_key_in_dict(key="long_description", book_raw=book_raw),
            "status": self.is_key_in_dict(key="status", book_raw=book_raw),
            "authors": self.is_key_in_dict(key="authors", book_raw=book_raw),
            "categories": self.is_key_in_dict(key="categories", book_raw=book_raw),
        })

    def is_key_in_dict(self, key: str, book_raw: Dict):
        return book_raw[key] if key in book_raw else None


class NoBookError(Exception):
    pass


class NoBookUpdateError(Exception):
    pass


class NoBookDeleteError(Exception):
    pass
