from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService, JobService
from ...models import JobLog
from ...schemas import JobLogBaseResponse, JobLogResponse, JobLogSerializerResponse


class JobLogService(BaseService):
    relationships = [JobLog.job]

    def __init__(self, session: AsyncSession):
        super().__init__(session, JobLog)
        self.job_service = JobService(session)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> JobLogBaseResponse:
        return JobLogBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> JobLogResponse:
        base_response = self._to_base_response(item)
        return JobLogResponse(
            **base_response.model_dump(),
            job_id=item.job_id
        )

    def _to_serialized_response(self, item) -> JobLogSerializerResponse:
        base_response = self._to_base_response(item)
        return JobLogSerializerResponse(
            **base_response.model_dump(),
            job=self.job_service._to_serialized_response(item.job),
        )
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///

