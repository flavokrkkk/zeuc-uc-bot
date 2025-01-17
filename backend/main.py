from fastapi import FastAPI

from backend.routers import api_router


app = FastAPI()


app.include_router(api_router)