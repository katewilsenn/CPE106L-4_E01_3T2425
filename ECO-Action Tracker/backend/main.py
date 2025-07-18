from fastapi import FastAPI
from backend.router import router

app = FastAPI()

app.include_router(router)
