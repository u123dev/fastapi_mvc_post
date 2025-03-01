from sqlalchemy import String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    _hashed_password: Mapped[str] = mapped_column("hashed_password", String(255), nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
