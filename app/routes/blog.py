from fastapi import APIRouter, Response, status
from repositories.blog import BlogRepository, BlogCreatePayload, BlogUpdatePayload

router = APIRouter()
blog_repo = BlogRepository(None)


def blog_router(repo):
    global blog_repo
    blog_repo = repo
    return router


@router.get("/blogs")
def read_blogs():
    blogs = blog_repo.find_all()
    return {
        "message": "ok",
        "data": blogs
    }


@router.get("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
def read_blog(blog_id: str, response: Response):
    blog = blog_repo.find_by_id(blog_id)
    return {
        "message": "ok",
        "data": blog
    }


@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog: BlogCreatePayload):
    new_blog_id = blog_repo.create(blog)
    return {
        "message": "ok",
        "data": {
            "blog_id": new_blog_id
        }
    }


@router.put("/blogs/{blog_id}", status_code=status.HTTP_200_OK)
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


@router.delete("/blogs/{blog_id}")
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
