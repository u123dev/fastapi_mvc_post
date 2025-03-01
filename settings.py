# Settings
API_VERSION_PREFIX = "/api/v1"
# DATABASE_URL = "mysql+pymysql://user:password@localhost/db_post"
DATABASE_URL = "sqlite:///./db_post.db"
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
POST_SIZE_LIMIT = 1024 * 1024  # 1 MB
CACHE_TIME = 300  # cache validity time in sec
