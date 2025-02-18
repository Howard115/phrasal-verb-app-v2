from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    BACKEND_URL: str = "https://phr-backend.hnd1.zeabur.app"
    FRONTEND_URL: str = "https://phr-frontend.hnd1.zeabur.app"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# API Documentation metadata
tags_metadata = [
    {
        "name": "authentication",
        "description": "Operations for user authentication with Google SSO"
    },
    {
        "name": "user_data",
        "description": "Operations with user's stored data"
    },
    {
        "name": "phrasal_verbs",
        "description": "Operations for retrieving phrasal verbs"
    }
] 