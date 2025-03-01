from cachetools import TTLCache
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from models import Post, User
from schemas import PostCreateSchema, PostResponseSchema, PostListResponseSchema
from repositories.post_repo import PostRepository

from settings import POST_SIZE_LIMIT, CACHE_TIME, API_VERSION_PREFIX

# Cache for posts
cache = TTLCache(maxsize=1000, ttl=CACHE_TIME)


def create_post(db: Session, post_data: PostCreateSchema, user: User) -> PostResponseSchema:
    """
    Create a new post for current user
    Validate text no more than POST_SIZE_LIMIT
    """
    if len(post_data.text.encode("utf-8")) > POST_SIZE_LIMIT:
        raise HTTPException(status_code=413, detail="Payload too large")

    try:
        new_post = PostRepository.create_post(db, post_data, user.id)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request.",
        )
    return PostResponseSchema.model_validate(new_post)


def remove_post(db: Session, post_id: int, user: User) -> dict:
    """
    Remove a post from current user
    """
    post = PostRepository.get_post_by_id(db, post_id, user.id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    try:
        PostRepository.delete_post(db, post)
        return {"detail": "Post deleted successfully."}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the post.",
        )


def list_posts(db: Session, user: User, page: int, per_page: int) -> PostListResponseSchema:
    """
    Paginated List all posts for current user
    with Caching for CACHE_TIME in sec
    """
    cache_key = f"posts_page_{page}_per_page_{per_page}_user_{user.id}"
    if cache_key in cache:
        print("..getting from cache")
        return cache[cache_key]

    posts, total_items = PostRepository.get_user_posts(db, user.id, page, per_page)

    if not posts:
        raise HTTPException(status_code=404, detail="No posts found.")

    post_list = [PostResponseSchema.model_validate(post) for post in posts]
    total_pages = (total_items + per_page - 1) // per_page

    response = PostListResponseSchema(
        posts=post_list,
        prev_page=f"{API_VERSION_PREFIX}/posts/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        next_page=f"{API_VERSION_PREFIX}/posts/?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items,
    )

    cache[cache_key] = response
    return response
