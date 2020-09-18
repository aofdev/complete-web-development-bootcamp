
from fastapi import APIRouter, Response, status
from repositories.movie import MovieRepository, NoMovieError, NoMovieUpdateError, NoMovieDeleteError
from entities.movie import Movie

router = APIRouter()
movie_repo = MovieRepository(None)


def movie_router(repo: MovieRepository):
    global movie_repo
    movie_repo = repo
    return router


@router.get("/")
def get_movies():
    pass


@router.get("/{movie_id}")
def get_movie(movie_id: str, response: Response):
    pass


@router.post("/")
def create_movie(movie: Movie, response: Response):
    pass


@router.put("/{movie_id}")
def update_movie(movie_id: str, movie: Movie, response: Response):
    pass


@router.delete("/{movie_id}")
def delete_movie(movie_id: str, response: Response):
    pass
