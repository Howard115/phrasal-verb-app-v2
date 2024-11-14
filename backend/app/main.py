from fastapi import FastAPI

from app.config import tags_metadata
from app.routers import auth, numbers, api_keys, phrasal_verbs

app = FastAPI(
    title="Phrasal Verbs API",
    description="An API service for generating stories with phrasal verbs",
    openapi_tags=tags_metadata
)

app.include_router(auth.router)
app.include_router(numbers.router)
app.include_router(api_keys.router)
app.include_router(phrasal_verbs.router)