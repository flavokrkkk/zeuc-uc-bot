from aiogram import Router
from handlers.commands import router as commands_router
from handlers.admin import router as admin_router
from handlers.menu import router as menu_router


router = Router()

router.include_router(commands_router)
router.include_router(admin_router)
router.include_router(menu_router)