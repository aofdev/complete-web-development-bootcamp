
from fastapi import APIRouter, Response, status
from repositories.book import BookRepository, NoBookError, NoBookUpdateError, NoBookDeleteError
from entities.book import Book

router = APIRouter()
book_repo = BookRepository(None)


def book_router(repo: BookRepository):
    global book_repo
    book_repo = repo
    return router


@router.get("/")
def read_books():
    books = book_repo.find_all()

    return {
        "message": "ok",
        "data": books
    }


@router.get("/{book_id}")
def read_book(book_id: str, response: Response):
    try:
        book = book_repo.find_by_id(book_id)
        return {
            "message": "ok",
            "data": [book]
        }
    except NoBookError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": f"book with id {book_id} is not found"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.post("/")
def create_book(book: Book, response: Response):
    try:
        created_book_id = book_repo.create(book)
        return {
            "message": "ok",
            "data": {
                "book_id": created_book_id
            }
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.put("/{book_id}")
def update_book(book_id: str, book: Book, response: Response):
    try:
        updated_book_id = book_repo.update(book_id, book)
        return {
            "message": "ok",
            "data": {
                "book_id": updated_book_id
            }
        }
    except NoBookUpdateError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No book is updated"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }


@router.delete("/{book_id}")
def delete_book(book_id: str, response: Response):
    try:
        deleted_book_id = book_repo.delete(book_id)
        return {
            "message": "ok",
            "data": {
                "book_id": deleted_book_id
            }
        }
    except NoBookDeleteError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "No book is deleted"
        }
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "something went wrong"
        }
