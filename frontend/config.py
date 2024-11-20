import os

class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

config = Config()
