from backend.database.models.models import Reward
from backend.dto.reward import DiscountModel
from backend.dto.user_dto import UpdateUserModel, UserDiscountModel, UserModel
from backend.errors.user_errors import UserNotFound
from backend.repositories import UserRepository


class UserService:
    repository: UserRepository
    
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user(self, tg_id: int) -> UserModel:
        user = await self.repository.get_item(tg_id)
        return UserModel.model_validate(user, from_attributes=True)
    
    async def update_user(self, tg_id: int, form: UpdateUserModel):
        await self.repository.update_item(tg_id, **form.model_dump())
    
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

    async def update_rewards(self, tg_id: int, reward: Reward) -> None:
        if reward.reward_type == "uc_code":
            pass # todo send uc after get in reward
        elif reward.reward_type == "discount":
            await self.repository.add_discount(tg_id, reward.discount_id)

