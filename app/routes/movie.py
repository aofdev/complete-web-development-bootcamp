
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
    movies = movie_repo.find_all()

    return {
        "message": "ok",
        "data": movies
    }


@router.get("/{movie_id}")
def get_movie(movie_id: str, response: Response):
    try:
        movie = movie_repo.find_by_id(movie_id)
        return {
            "message": "ok",
            "data": [movie]
        }
    except NoMovieError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"movie with id {movie_id} is not found"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.post("/")
def create_movie(movie: Movie, response: Response):
    try:
        created_movie_id = movie_repo.create(movie)
        return {
            "message": "ok",
            "data": {
                "movie_id": created_movie_id
            }
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.put("/{movie_id}")
def update_movie(movie_id: str, movie: Movie, response: Response):
    try:
        updated_movie_id = movie_repo.update(movie_id, movie)
        return {
            "message": "ok",
            "data": {
                "movie_id": updated_movie_id
            }
        }
    except NoMovieUpdateError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No movie is updated"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.delete("/{movie_id}")
def delete_movie(movie_id: str, response: Response):
    try:
        deleted_movie_id = movie_repo.delete(movie_id)
        return {
            "message": "ok",
            "data": {
                "movie_id": deleted_movie_id
            }
        }
    except NoMovieDeleteError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No movie is deleted"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }
