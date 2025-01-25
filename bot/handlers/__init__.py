from aiogram import Router
from handlers.commands import router as commands_router
from handlers.uc_codes import router as uc_codes_router
from handlers.menu import router as menu_router
from handlers.prices import router as prices_router
from handlers.stats import router as stats_router


router = Router()


router.include_router(commands_router)
router.include_router(uc_codes_router)
router.include_router(menu_router)
router.include_router(prices_router)
router.include_router(stats_router)