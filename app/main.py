from fastapi import FastAPI, Header, HTTPException, Depends,  Response
from pymongo import MongoClient


from entities.blog import Blog
from entities.book import Book
from repositories.blog import BlogRepository, BlogCreatePayload, BlogUpdatePayload
from repositories.book import BookRepository, NoBookError
from routes.book import book_router
from routes.blog import blog_router


app = FastAPI()
client = MongoClient("mongodb://cwdb101:!cwdb101!@localhost:27020")
blog_repo = BlogRepository(client["bootcamp"]["blogs"])
book_repo = BookRepository(client["bootcamp"]["books"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Complete Web Developer Bootcamp 2020"}


def get_token_header(api_key: str = Header(...)):
    if api_key != "complete-web-developer-bootcamp-2020":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(
    blog_router(blog_repo),
    prefix="/blogs",
    tags=["blogs"],
    dependencies=[Depends(get_token_header)],
)

app.include_router(
    book_router(book_repo),
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_token_header)]
)
