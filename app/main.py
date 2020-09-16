from typing import Optional
from datetime import date
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

# from library import Library, Book, NoBookError
from app.entities.blog import BlogRepository, Blog, BlogCreatePayload, BlogUpdatePayload
from app.entities.book import Book
from app.repositories.book import BookRepository


app = FastAPI()
# library = Library()
client = MongoClient("mongodb://root:root@localhost:27020")
# blog_repo = BlogRepository(client["bootcamp"]["blogs"])
book_repo = BookRepository(client["bootcamp"]["books"])


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/blogs")
# def read_blogs():
#     blogs = blog_repo.find_all()
#     return {
#         "message": "ok",
#         "data": blogs
#     }


# @app.get("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
# def read_blog(blog_id: str, response: Response):
#     blog = blog_repo.find_by_id(blog_id)
#     return {
#         "message": "ok",
#         "data": blog
#     }


# @app.post("/blogs", status_code=status.HTTP_201_CREATED)
# def create_blog(blog: BlogCreatePayload):
#     new_blog_id = blog_repo.create(blog)
#     return {
#         "message": "ok",
#         "data": {
#             "blog_id": new_blog_id
#         }
#     }


# @app.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
# def update_blog(blog_id: str, blog: BlogUpdatePayload, response: Response):
#     try:
#         updated_blog_id = blog_repo.update(blog_id, blog)
#         return {
#             "message": "ok",
#             "data": {
#                 "blog_id": blog_id
#             }
#         }
#     except NoBookError:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {
#             "message": f"blog {blog_id} not found"
#         }
#     except Exception as e:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {
#             "message": str(e),
#         }


# @app.delete("/blogs/{blog_id}")
# def delete_blog(blog_id: int, response: Response):
#     try:
#         blog_repo.delete(blog_id)
#         return {
#             "message": "ok",
#         }
#     except NoBookError:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {
#             "message": f"blog {blog_id} not found"
#         }
#     except Exception as e:
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {
#             "message": str(e)
#         }


@app.get("/books")
def read_books():
    books = book_repo.find_all()
    return {
        "message": "ok",
        "data": books
    }


@app.get("/books/{book_id}")
def read_book(book_id: int, response: Response):
    try:
        book = book_repo.find(id)
        return {
            "message": "ok",
            "data": [book]
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"something went wrong {str(e)}"
        }


@app.post("/books")
def create_book(book: Book, response: Response):
    try:
        created_book_id = book_repo.create(book)
        return {
            "message": "ok",
            "data": {
                "book_id": created_book_id
            }
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"something went wrong {str(e)}"
        }
