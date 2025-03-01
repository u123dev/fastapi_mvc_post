from datetime import datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from jose import JWTError, jwt

from models import User
from settings import DATABASE_URL, SECRET_KEY, ALGORITHM


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    """ Get db """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


# check token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """ Get current user by jwt token & validate token expiration """
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        exp = payload.get("exp")
        if id is None or exp is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        if datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        print(f"JWT Error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
