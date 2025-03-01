from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from repositories.user_repo import UserRepository
from services.security import hash_password, create_access_token, verify_password
from schemas import UserSignupSchema, UserResponseSchema


def register(db: Session, user_data: UserSignupSchema) -> UserResponseSchema:
    """ Register a new user by email & password and return - jwt token"""
    if UserRepository.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user_data.password)

    try:
        new_user = UserRepository.create_user(db, user_data.email, hashed_password)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the request.",
        )

    access_token = create_access_token(new_user.id)
    return UserResponseSchema(access_token=access_token)


def login_user(db: Session, user_data: OAuth2PasswordRequestForm) -> UserResponseSchema:
    """ Login a user by email & password and return - jwt token"""
    db_user = UserRepository.get_user_by_email(db, user_data.username)
    if not db_user or not verify_password(user_data.password, db_user._hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(db_user.id)
    return UserResponseSchema(access_token=access_token)
