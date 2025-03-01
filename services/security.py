from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from models import User
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


# Hash for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# for passwords
def hash_password(password: str) -> str:
    """ Hashes a password using SHA512 """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Checks if the password matches the given password """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, expires_delta: timedelta = None) -> str:
    """ Creates a JWT access token with the given user ID & expiration """
    if expires_delta is None:
        expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
