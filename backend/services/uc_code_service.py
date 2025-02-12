from backend.database.models.models import UCCode
from backend.dto.uc_code_dto import CreateUCCodeModel, UCCodeModel, UCPackModel
from backend.errors.uc_code_errors import UCCodeAlreadyExists, UCCodeNotFound
from backend.repositories.uc_code_repository import UCCodeRepository


class UCCodeService:
    def __init__(self, repository: UCCodeRepository):
        self.repository = repository

    async def create(self, form: CreateUCCodeModel) -> UCCodeModel:
        uc_code = await self.repository.get_item(form.code)
        if uc_code:
            raise UCCodeAlreadyExists
        
        uc_code = await self.repository.add_item(**form.model_dump())
        return UCCodeModel.model_validate(uc_code, from_attributes=True)
    
    async def get_uc_code(self, code: str) -> UCCodeModel:
        uc_code = await self.repository.get_item(code)
        if not uc_code:
            raise UCCodeNotFound
        return UCCodeModel.model_validate(uc_code, from_attributes=True)
    
    async def delete_uc_code(self, code: str) -> None:
        code = await self.repository.get_item(code)
        if not code:
            raise UCCodeNotFound
        await self.repository.delete_item(code.code)
    
    async def delete_codes(self, codes: list[str]) -> None:
        for code in codes:
            code = await self.repository.get_item(code)
            if not code:
                continue
            await self.repository.delete_item(code.code)

    async def delete_by_value(self, value: str) -> None:
        codes = await self.repository.get_by_attributes((self.repository.model.value, value))
        for code in codes:
            await self.repository.delete_item(code.code)

    async def get_by_value(self, value: str) -> list[UCCodeModel]:
        codes = await self.repository.get_by_attributes((self.repository.model.value, value))
        return [
            UCCodeModel.model_validate(code, from_attributes=True) 
            for code in codes
        ]
    
    async def group_by_amount(self) -> list[UCCodeModel]:
        codes = await self.repository.group_by_amount()
        return [
            UCCodeModel(
                uc_amount=uc_amount, 
                price_per_uc=float(price), 
                quantity=quantity,
                point=point
            ) 
            for uc_amount, price, quantity, point in codes
        ]
    
    async def get_uc_packs_bonuses_sum(self, uc_packs: list[UCPackModel]) -> int:
        bonuses = 0
        for uc_pack in uc_packs:
            point = await self.repository.get_point_by_uc_amount(uc_pack.uc_amount)
            bonuses += point
        return bonuses