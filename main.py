from fastapi import FastAPI

from app.endpoints.secrets import secrets

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(secrets)
