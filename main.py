from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints.secrets import secrets

from dotenv import load_dotenv

load_dotenv()
origins = ["http://localhost:8000"]

app = FastAPI()
app.include_router(secrets)
app.add_middleware(CORSMiddleware, allow_origins=origins)
