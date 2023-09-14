from fastapi import FastAPI

from app.endpoints.secrets import secrets

app = FastAPI()
app.include_router(secrets)
