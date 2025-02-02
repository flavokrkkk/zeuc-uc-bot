from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from backend.database.connection.connection import DatabaseConnection
from backend.middlewares.decode_middleware import DecodeEncodeMiddleware
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
        "https://zeusucbot.shop/",
        "https://zeusucbot.shop",
        "http://213.226.127.164/",
        "http://213.226.127.164",
        "https://83.222.9.37",
        "83.222.9.37",
        "http://83.222.9.37",   
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(DecodeEncodeMiddleware)