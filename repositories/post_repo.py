from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Post
from schemas import PostCreateSchema


class PostRepository:
    @staticmethod
    def create_post(db: Session, post_data: PostCreateSchema, user_id: int) -> Post:
        """ Add a post to the database"""
        new_post = Post(text=post_data.text, user_id=user_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post

    @staticmethod
    def get_post_by_id(db: Session, post_id: int, user_id: int):
        """ Get a post from the database"""
        return db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()

    @staticmethod
    def delete_post(db: Session, post: Post):
        """ Delete a post from the database"""
        db.delete(post)
        db.commit()

    @staticmethod
    def get_user_posts(db: Session, user_id: int, page: int, per_page: int):
        """ Get all posts from a user"""
        offset = (page - 1) * per_page

        # query = db.query(Post).filter(Post.user_id == user_id)
        # total_items = query.count()
        # posts = query.offset(offset).limit(per_page).all()

        query = db.query(
            Post,
            func.count(Post.id).over().label("total_items")
        ).filter(Post.user_id == user_id)
        results = query.offset(offset).limit(per_page).all()
        posts = [result[0] for result in results]
        total_items = results[0].total_items if results else 0

        return posts, total_items
