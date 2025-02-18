from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import JobLog


class JobLogService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, JobLog)
