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
        "https://frontend-aat1h29kv-flavokrkkks-projects.vercel.app",
        "https://frontend-pink-alpha-31.vercel.app",
        "http://81.177.221.219/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(DecodeEncodeMiddleware)