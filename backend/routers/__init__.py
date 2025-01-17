from fastapi import APIRouter
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router


router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(users_router)