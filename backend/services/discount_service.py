from backend.dto.reward import DiscountModel
from backend.dto.user_dto import UserDiscountModel
from backend.errors.user_errors import UserDiscountNotFound
from backend.repositories.discount_repository import DiscountRepository


class DiscountService:
    def __init__(self, repository: DiscountRepository):
        self.repository = repository

    async def get_user_discounts(self, tg_id: int) -> list[UserDiscountModel]:
        user_discounts = await self.repository.get_user_discounts(tg_id=tg_id)
        return [
            UserDiscountModel(
                discount=DiscountModel.model_validate(
                    await self.repository.get_item(user_discount.discount_id), 
                    from_attributes=True
                ),
                count=user_discount.count
            )
            for user_discount in user_discounts
        ]

    async def delete_discount_from_user(self, tg_id: int, discount_id: int) -> int:
        discount = await self.repository.delete_discount_from_user(
            tg_id=tg_id, 
            discount_id=discount_id
        )
        if not discount:
            raise UserDiscountNotFound
        discount_id = discount
        return discount