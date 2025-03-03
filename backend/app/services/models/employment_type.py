from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import EmploymentType
from ...schemas import EmploymentTypeBaseResponse, EmploymentTypeResponse, EmploymentTypeSerializerResponse


class EmploymentTypeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EmploymentType)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> EmploymentTypeBaseResponse:
        return EmploymentTypeBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> EmploymentTypeResponse:
        base_response = self._to_base_response(item)
        return EmploymentTypeResponse(**base_response.model_dump())

    def _to_serialized_response(self, item) -> EmploymentTypeSerializerResponse:
        base_response = self._to_base_response(item)
        return EmploymentTypeSerializerResponse(**base_response.model_dump())
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///