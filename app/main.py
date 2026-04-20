from fastapi import FastAPI
from app.api.v1.api import api_router
from app.api.errors import setup_exceptions_handlers

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

setup_exceptions_handlers(app)