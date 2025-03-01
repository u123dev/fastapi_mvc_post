from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from models import User
from dependencies import get_db
from schemas import UserSignupSchema, UserLoginSchema, UserResponseSchema
from services.security import hash_password, create_access_token, verify_password
from services.user_service import register, login_user

router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="User Registration",
    description="<H3>Register a new user with an email and password.</H3>",
)
def signup(user: UserSignupSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    return register(db, user)


@router.post(
    "/login",
    response_model=UserResponseSchema,
    summary="User Login",
    description="<H3>Authenticate a user and return access token & token type.</H3>",
    status_code=status.HTTP_201_CREATED,
)
def login(
        user: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
) -> UserResponseSchema:
    return login_user(db, user)
