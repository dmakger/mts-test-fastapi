from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import EmploymentType


class EmploymentTypeService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EmploymentType)
