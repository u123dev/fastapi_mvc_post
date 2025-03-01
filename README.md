## FastAPI Web application following the MVC design pattern.
- 3 different Levels for **Routing**, **Business Logic**, DB calls (**Repositories**) for each call Functionality.
- Interface with a SQLite / MySQL database using SQLAlchemy for ORM.
- Field validation and dependency injection.


### Endpoints:

-  **Signup** Endpoint:
    Accepts `email` and `password`.
    Returns a token JWT.

-  **Login** Endpoint:
    Accepts `email` and `password`.
    Returns a token upon successful login; error response if login fails.

-  **AddPost** Endpoint:
    Accepts `text` and a `token` for authentication.
    Validates payload size (limit to 1 MB), saves the post in memory, returning `postID`.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.
  
-  **GetPosts** Endpoint:
    Requires a token for authentication.
    Returns all user's posts.
    Implements response caching for up to 5 minutes for the same user.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.

-  **DeletePost** Endpoint:
    Accepts `postID` and a `token` for authentication.
    Deletes the corresponding post from memory.
    Returns an error for invalid or missing token.
    Dependency injection for token authentication.


### Additional Notes:

-  Utilizing token-based authentication for the "AddPost" and "GetPosts" endpoints, obtainable from the "Login" endpoint.
-  Implementing request validation for the "AddPost" endpoint to ensure the payload does not exceed 1 MB.
-  Using in-memory caching for "GetPosts" to cache data for up to 5 minutes.
-  Implementation of both SQLAlchemy and Pydantic models for each endpoint includes extensive type validation to guarantee the accuracy and integrity of data being processed.

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Cachetool
- JWT Token

## Project Directory Structure

```plaintext
.
├── models
│   ├── __init__.py
│   ├── base.py
│   ├── posts.py
│   └── users.py
├── schemas
│   ├── __init__.py
│   ├── posts.py
│   └── users.py
├── repositories
│   ├── post_repo.py
│   └── user_repo.py
├── services
│   ├── post_service.py
│   ├── user_service.py
│   └── security.py
├── routes
│   ├── __init__.py
│   ├── posts.py
│   └── users.py
├── dependencies.py
├── settings.py
├── create_tables.py
├── main.py
├── requirements.txt
└── README.md
```



### How to run

1. Clone this repository
   ```sh
    git clone https://github.com/u123dev/fastapi_mvc_post.git
    ```
2. Open the project folder in IDE or 
    ```
    cd fastapi_mvc_post
    ```
3. Make virtual environment:
    ```
    py -m venv venv
    venv\Scripts\activate (on Windows)
    # or
    source venv/bin/activate (on macOS)
    ```
4. Dependency install
    ```sh
    pip install -r requirements.txt
    ```
5. Start Server
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
6. Create database & tables (for first run)
   ```
   python create_tables.py
   ```

### API Access docs
   - [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

### Contact
Feel free to contact: u123@ua.fm
