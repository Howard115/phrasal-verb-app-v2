import os
from urllib.parse import urlparse

class Config:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

    @property
    def backend_origin(self):
        parsed = urlparse(self.BACKEND_URL)
        return f"{parsed.scheme}://{parsed.netloc}"

    @property
    def frontend_origin(self):
        parsed = urlparse(self.FRONTEND_URL)
        return f"{parsed.scheme}://{parsed.netloc}"

config = Config()
