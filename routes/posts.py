from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session

from starlette import status

from models import User, Post
from services.post_service import create_post, remove_post, list_posts

from dependencies import get_current_user, get_db
from schemas import PostCreateSchema, PostResponseSchema, PostListResponseSchema


router = APIRouter()


@router.post(
    "/add_post",
    response_model=PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new post",
    description=(
            "<h3>This endpoint allows user to add a new post to the database. <BR> "
            "It accepts details such as id, post content, associated user(owner) id. </h3>"
    ),
)
def add_post(
        post: PostCreateSchema,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> PostResponseSchema:
    return create_post(db, post, user)


@router.get(
    "/get_posts",
    response_model=PostListResponseSchema,
    summary="Get a paginated list of posts",
    description=(
            "<h3>This endpoint retrieves a paginated list of posts for current user from the database. <br>"
            "User can specify the `page` number and the number of items per page using `per_page`. <br>"
            "The response includes details about the posts, total pages, and total items, "
            "along with links to the previous and next pages if applicable.</h3>"
    ),
)
def get_posts(
        page: int = Query(1, ge=1, description="Page number (1-based index)"),
        per_page: int = Query(10, ge=1, le=20, description="Number of items per page"),
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
) -> PostListResponseSchema:
    return list_posts(db, user, page, per_page)


@router.delete(
    "/delete_post",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a post by ID",
    description=(
            "<h3>Delete a specific post from the database by its unique ID.</h3>"
            "<p>If the post exists, it will be deleted. If it does not exist, "
            "a 404 error will be returned.</p>"
    ),
)
def delete_post(postID: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return remove_post(db, postID, user)
