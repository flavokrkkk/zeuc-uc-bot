from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from backend.database.connection.connection import DatabaseConnection
from backend.middleware.decode_middleware import DecodeEncodeMiddleware
from backend.routers import api_router


async def lifespan(app: FastAPI):
    db_connection = await DatabaseConnection()()
    app.state.db_connection = db_connection
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://81.177.221.219",
        "http://81.177.221.219:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(DecodeEncodeMiddleware)