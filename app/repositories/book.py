
from pymongo.collection import Collection
from app.entities.book import Book


class BookRepository():
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_all(self):
        books = [Book(**book_raw.dict())
                 for book_raw in self.collection.find()]
        return books

    def find_by_id(self, id: int):
        book_raw = self.collection.find_one({"_id": id})
        book = Book(**book_raw)
        return book

    def create(self, book: Book):
        inserted_result = self.collection.insert_one(book.dict())
        inserted_id = inserted_result.inserted_id
        return inserted_id

    def update(self, id: int, book: Book):
        updated_result = self.collection.update_one(
            {"_id": id}, book.dict(exclude_unset=True))
        updated_id = updated_result.upserted_id
        return updated_id

    def delete(self, id: int):
        deleted_result = self.collection.delete_one({"_id": id})
        return id
