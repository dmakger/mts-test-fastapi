from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService, LevelService
from ...models import Position
from ...schemas import PositionBaseResponse, PositionResponse, PositionSerializerResponse


class PositionService(BaseService):
    relationships = [Position.level]

    def __init__(self, session: AsyncSession):
        super().__init__(session, Position)
        self.level_service = LevelService(session)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> PositionBaseResponse:
        return PositionBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> PositionResponse:
        base_response = self._to_base_response(item)
        return PositionResponse(
            **base_response.model_dump(),
            level_id=item.level_id
        )

    def _to_serialized_response(self, item) -> PositionSerializerResponse:
        base_response = self._to_base_response(item)
        return PositionSerializerResponse(
            **base_response.model_dump(),
            level=self.level_service._to_serialized_response(item.level),
        )
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///

