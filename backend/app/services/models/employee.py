from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import Employee
from ...schemas import EmployeeBaseResponse, EmployeeResponse, EmployeeSerializerResponse


class EmployeeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Employee)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> EmployeeBaseResponse:
        return EmployeeBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> EmployeeResponse:
        base_response = self._to_base_response(item)
        return EmployeeResponse(**base_response.model_dump())

    def _to_serialized_response(self, item) -> EmployeeSerializerResponse:
        base_response = self._to_base_response(item)
        return EmployeeSerializerResponse(**base_response.model_dump())
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///
