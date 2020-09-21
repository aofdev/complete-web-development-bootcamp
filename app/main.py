import os
from fastapi import FastAPI, Header, HTTPException, Depends, Response
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient

from entities.book import Book
from repositories.book import BookRepository
from routes.book import book_router

from entities.movie import Movie
from repositories.movie import MovieRepository
from routes.movie import movie_router

from repositories.async_book import AsyncBookRepository
from routes.async_book import async_book_router


import motor.motor_asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Local
MONGO_URI = "mongodb://cwdb101:!cwdb101!@localhost:27020"

# Get Config Production
if 'PRODUCTION' in os.environ:
    MONGO_URI = os.environ['PRODUCTION']

client = MongoClient(MONGO_URI)
book_repo = BookRepository(collection=client["bootcamp"]["books"])
movie_repo = MovieRepository(collection=client["bootcamp"]["movies"])


async_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
async_book_repo = AsyncBookRepository(
    collection=async_client["bootcamp"]["books"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Complete Web Developer Bootcamp 2020"}


async def get_token_header(api_key: str = Header(...)):
    if api_key != "complete-web-developer-bootcamp-2020":
        raise HTTPException(
            status_code=400, detail="api-key header invalid")


app.include_router(
    book_router(book_repo),
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_token_header)]
)

app.include_router(
    movie_router(movie_repo),
    prefix="/movies",
    tags=["movies"],
    dependencies=[Depends(get_token_header)]
)


app.include_router(
    async_book_router(async_book_repo),
    prefix="/async_books",
    tags=["async_books"],
    dependencies=[Depends(get_token_header)]
)
