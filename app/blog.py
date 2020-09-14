from typing import Dict
from pydantic import BaseModel
from datetime import datetime
from pymongo.collection import Collection
from bson.objectid import ObjectId


class Blog(BaseModel):
    id: str
    title: str
    body: str
    author: str
    cover_image_url: str
    created_date: datetime
    last_edited_date: datetime


class BlogRepository():
    def __init__(self, collection: Collection):
        self.collection = collection

    def find_all(self):
        blogs_raw = [blog_raw for blog_raw in self.collection.find()]
        blogs = list(
            map(lambda blog_raw: self.map_raw_to_blog(blog_raw), blogs_raw))
        return blogs

    def find_by_id(self, id: str):
        blog_raw = self.collection.find_one({"_id": ObjectId(id)})
        return self.map_raw_to_blog(blog_raw)

    def map_raw_to_blog(self, blog_raw: Dict):
        return Blog(**{
            "id": str(blog_raw["_id"]),
            "title": blog_raw["title"],
            "body": blog_raw["body"],
            "author": blog_raw["author"],
            "cover_image_url": blog_raw["cover_image_url"],
            "created_date": blog_raw["created_date"],
            "last_edited_date": blog_raw["last_edited_date"]
        })
