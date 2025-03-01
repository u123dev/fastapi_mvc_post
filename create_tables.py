from database.db import engine, Base
from database.models import User, Post


def create_tables():
    """
    Create tables if not exists
    """

    print("Creating table in db ...")
    try:
        User.__table__.create(bind=engine)
        Post.__table__.create(bind=engine)
        print("Tables are created")
    except Exception as e:
        print(f"Error in creating tables: {e}")


if __name__ == "__main__":
    create_tables()
