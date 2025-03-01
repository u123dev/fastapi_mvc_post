from sqlalchemy.orm import Session
from models import User


class UserRepository:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """ Get a user from database by email """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, email: str, hashed_password: str) -> User:
        """ Add new user to database """
        new_user = User(email=email, _hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
