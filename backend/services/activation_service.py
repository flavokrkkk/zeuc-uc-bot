from aiohttp import ClientSession
from backend.dto.activation_dto import ActivationModel, CreateActivationModel
from backend.dto.activation_dto import UCActivationResult
from backend.errors.activation_errors import ActivationNotFound
from backend.repositories.activation_repository import ActivationRepository


class ActivationService:
    def __init__(self, repository: ActivationRepository):
        self.repository = repository
        self.api_url: str = "https://ucodeium.com/api/activate"
        
    async def _post_request(self, payload: dict[str, str | int]) -> UCActivationResult:
        headers: dict[str, str] = {"X-Api-Key": self.api_key}
        async with ClientSession(timeout=self.timeout) as session:
            async with session.post(
                self.api_url,
                headers=headers,
                json=payload,
                ssl=False,
            ) as response:
                if response.status == 200:
                    api_response = await response.json()
                    return UCActivationResult(success=1, response=api_response)
                return UCActivationResult(success=0, response={})

    async def activate_code(self, payload: CreateActivationModel) -> None:
        result: UCActivationResult = await self._post_request(payload)
        return result.model_dump()

    async def create(self, form: CreateActivationModel) -> ActivationModel:
        activation = await self.repository.get_item(form.activation_id)
        if not activation:
            activation = await self.repository.add_item(**form.model_dump())
        return ActivationModel.model_validate(activation, from_attributes=True)
    
    async def delete_by_id(self, activation_id: str) -> None:
        activation = await self.repository.get_item(activation_id)
        if not activation:
              return ActivationNotFound
        await self.repository.delete_item(activation_id)

    async def get_by_tg_id(self, activation_id: str) -> ActivationModel:
        activation = await self.repository.get_by_attributes(
            (self.repository.model.activation_id, activation_id)
        )
        if not activation:
            return ActivationNotFound
        return ActivationModel.model_validate(activation, from_attributes=True)
    
    async def get_by_value(self, value: str) -> list[ActivationModel]:
        activations = await self.repository.get_by_attributes(
            (self.repository.model.value, value)
        )
        return [
            ActivationModel.model_validate(activation, from_attributes=True) 
            for activation in activations
        ]
    
    async def count_by_value(self, value: str) -> int:
        activations = await self.repository.get_by_attributes(
            (self.repository.model.value, value)
        )
        return len(activations)
    
    async def get_between_by_value(self, value: int, start: int, end: int) -> list[ActivationModel]:
        activations = await self.repository.get_between_by_value(value, start, end)
        return [
            ActivationModel.model_validate(activation, from_attributes=True) 
            for activation in activations
        ]
    
    async def count_between_by_value(self, value: int, start: int, end: int) -> int:
        activations = await self.repository.get_between_by_value(value, start, end)
        return len(activations)