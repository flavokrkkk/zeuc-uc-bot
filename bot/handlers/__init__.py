from aiogram import Router
from handlers.commands import router as commands_router
from handlers.uc_codes import router as uc_codes_router
from handlers.stats import router as stats_router
from handlers.off_or_on_store import router as off_or_on_store_router
from handlers.black_list import router as black_list_router
from handlers.purchases import router as payment_router
from handlers.bonuses import router as bonuses_router
from handlers.rewards import router as rewards_router
from handlers.user_rewards import router as user_rewards_router


router = Router()


router.include_router(commands_router)
router.include_router(uc_codes_router)
router.include_router(stats_router)
router.include_router(off_or_on_store_router)
router.include_router(black_list_router)
router.include_router(payment_router)
router.include_router(bonuses_router)
router.include_router(rewards_router)
router.include_router(user_rewards_router)