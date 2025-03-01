from fastapi import FastAPI


from routes import (
    users_router,
    posts_router,
)
from settings import API_VERSION_PREFIX


app = FastAPI(
    title="Post management API",
    description="Description of project"
)


app.include_router(users_router, prefix=f"{API_VERSION_PREFIX}/users", tags=["users"])
app.include_router(posts_router, prefix=f"{API_VERSION_PREFIX}/posts", tags=["posts"])
