from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService, LevelService
from ...models import Division
from ...schemas import DivisionBaseResponse, DivisionResponse, DivisionSerializerResponse


class DivisionService(BaseService):
    relationships = [Division.level]

    def __init__(self, session: AsyncSession):
        super().__init__(session, Division)
        self.level_service = LevelService(session)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> DivisionBaseResponse:
        return DivisionBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> DivisionResponse:
        base_response = self._to_base_response(item)
        return DivisionResponse(
            **base_response.model_dump(),
            level_id=item.level_id,
            parent_id=item.parent_id,
        )

    def _to_serialized_response(self, item) -> DivisionSerializerResponse:
        base_response = self._to_base_response(item)
        return DivisionSerializerResponse(
            **base_response.model_dump(),
            level=self.level_service._to_serialized_response(item.level),
            parent_id=item.parent_id,
        )
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///
