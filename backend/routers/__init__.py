from fastapi import APIRouter, Depends
from backend.routers.auth import router as auth_router
from backend.routers.users import router as users_router
from backend.routers.uc_code import router as uc_code_router
from backend.routers.reward import router as reward_router
from backend.utils.dependencies.dependencies import get_current_user_dependency, get_store_is_on

PROTECTED = Depends(get_current_user_dependency)
STORE_IS_ON = Depends(get_store_is_on)


api_router = APIRouter(
    prefix="/api", 
    dependencies=[STORE_IS_ON]
)


api_router.include_router(auth_router)
api_router.include_router(users_router, dependencies=[PROTECTED])
api_router.include_router(uc_code_router, dependencies=[PROTECTED])
api_router.include_router(reward_router, dependencies=[PROTECTED])