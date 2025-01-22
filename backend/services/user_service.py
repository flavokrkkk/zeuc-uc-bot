from backend.database.models.models import Reward, User
from backend.dto.user_dto import BonusesHistoryModel, UserModel
from backend.errors.user_errors import UserAlreadyActivateReferal, UserNotFound, UserReferalCodeNotFound
from backend.repositories import UserRepository
from backend.utils.config.constants import BONUC_CIRCLE_PRICE
from backend.utils.config.enums import BonusStatuses


class UserService:
    repository: UserRepository
    
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user(self, tg_id: int) -> UserModel:
        user = await self.repository.get_item(tg_id)
        return UserModel.model_validate(user, from_attributes=True)
    
    async def update_user(self, tg_id: int, **kwargs) -> UserModel:
        await self.repository.update_item(tg_id, **kwargs)
    
    async def get_by_username(self, username: str) -> UserModel:
        user = await self.repository.get_by_attributes(
            (self.repository.model.username, username),
            one_or_none=True
        )
        return UserModel.model_validate(user, from_attributes=True)
    
    async def get_all_users(self) -> list[UserModel]:
        users = await self.repository.get_all_items()
        return [
            UserModel.model_validate(user, from_attributes=True) 
            for user in users
        ]
    
    async def set_admin_status(self, tg_id: int, is_admin: bool) -> None:
        await self.repository.update_item(
            self.repository.model.tg_id, 
            item_id=tg_id, 
            is_admin=is_admin
        )

    async def get_admin_users(self) -> list[UserModel]:
        users = await self.repository.get_by_attributes((self.repository.model.is_admin, True))
        return [
            UserModel.model_validate(user, from_attributes=True) 
            for user in users
        ]
        
    async def delete_user(self, tg_id: int) -> None:
        user = await self.repository.get_item(tg_id)
        if not user:
            raise UserNotFound
        await self.repository.delete_item(tg_id)

    async def update_rewards(self, user: UserModel, reward: Reward) -> None:
        await self.repository.add_discount(user.tg_id, reward.discount_id)
        await self.repository.update_item(
            self.repository.model.tg_id,
            user.tg_id, 
            bonuses=user.balance - BONUC_CIRCLE_PRICE
        )

    async def activate_referal_code(self, current_user: UserModel, referal_code: str) -> None:
        if current_user.referer_id:
            raise UserAlreadyActivateReferal
        
        referer: User = await self.repository.get_by_attributes(
            (self.repository.model.referal_code, referal_code),
            one_or_none=True
        )
        if not referer or referer.tg_id == current_user.tg_id:
            raise UserReferalCodeNotFound
    
        await self.repository.update_item(
            self.repository.model.tg_id,
            item_id=referer.tg_id,
            bonuses=referer.bonuses + 20
        )
        await self.repository.update_item(
            self.repository.model.tg_id,
            item_id=current_user.tg_id,
            referer_id=referer.tg_id,
            bonuses=current_user.bonuses + 20
        )
    
    async def send_bonuses_to_referer(self, user_id: int, bonuses: int) -> None:
        current_user: User = await self.repository.get_item(user_id)
        referer_user: User = await self.repository.get_item(current_user.referer_id)
        if referer_user and current_user.referer_id:
            await self.repository.add_bonuses(
                current_user.referer_id, 
                    bonuses, 
                BonusStatuses.GET.value
            )

    async def get_user_bonuses_history(self, tg_id: int):
        user: User = await self.repository.get_item(tg_id)
        return [
            BonusesHistoryModel.model_validate(bonus, from_attributes=True)
            for bonus in user.bonuses_history
        ]