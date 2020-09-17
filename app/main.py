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


app = FastAPI()
client = MongoClient("mongodb://cwdb101:!cwdb101!@localhost:27020")
blog_repo = BlogRepository(client["bootcamp"]["blogs"])
book_repo = BookRepository(client["bootcamp"]["books"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/blogs")
def read_blogs():
    blogs = blog_repo.find_all()
    return {
        "message": "ok",
        "data": blogs
    }


@app.get("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def read_blog(blog_id: str, response: Response):
    blog = blog_repo.find_by_id(blog_id)
    return {
        "message": "ok",
        "data": blog
    }


@app.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreatePayload):
    new_blog_id = blog_repo.create(blog)
    return {
        "message": "ok",
        "data": {
            "blog_id": new_blog_id
        }
    }


@app.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def update_blog(blog_id: str, blog: BlogUpdatePayload, response: Response):
    try:
        updated_blog_id = blog_repo.update(blog_id, blog)
        return {
            "message": "ok",
            "data": {
                "blog_id": blog_id
            }
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": str(e),
        }


@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int, response: Response):
    try:
        blog_repo.delete(blog_id)
        return {
            "message": "ok",
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": str(e)
        }


app.include_router(
    book_router(book_repo),
    prefix="/books",
    tags=["books"],
)
