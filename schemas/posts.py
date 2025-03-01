from typing import List

from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    text: str


class PostResponseSchema(BaseModel):
    id: int
    text: str
    # user_id: int

    model_config = {
        "from_attributes": True,
    }


class PostListResponseSchema(BaseModel):
    posts: List[PostResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int

    model_config = {
        "from_attributes": True,

    }
