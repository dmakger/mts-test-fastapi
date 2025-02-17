from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.app.models.job_log import JobLog


class JobLogService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, job_id: int, column_name: str, new_value: str, old_value: str = None):
        """Ищет или создает новый журнал работы"""
        stmt = select(JobLog).where(
            JobLog.job_id == job_id,
            JobLog.column_name == column_name,
            JobLog.new_value == new_value
        )
        result = await self.session.execute(stmt)
        job_log = result.scalars().first()

        if not job_log:
            job_log = JobLog(
                job_id=job_id,
                column_name=column_name,
                old_value=old_value,
                new_value=new_value
            )
            self.session.add(job_log)
            await self.session.commit()
            await self.session.refresh(job_log)

        return job_log
