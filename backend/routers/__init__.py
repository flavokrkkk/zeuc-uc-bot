from fastapi import APIRouter
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router


api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(users_router)