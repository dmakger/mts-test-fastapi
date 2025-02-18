from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import Division


class DivisionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Division)
