from fastapi import APIRouter, Depends
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.uc_code import router as uc_code_router
from backend.routers.reward import router as reward_router
from backend.utils.dependencies.dependencies import get_current_user_dependency


api_router = APIRouter(
    prefix="/api", 
    # dependencies=[Depends(get_current_user_dependency)]
)

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(uc_code_router)
api_router.include_router(reward_router)
