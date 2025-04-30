import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8080")
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = False  # True in production
