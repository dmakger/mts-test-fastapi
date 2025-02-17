from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from ..models.job import Job


class JobService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, employee_id: int, employment_type_id: int, position_id: int, division_id: int, hire_date: str, salary: float):
        """Ищет работу или создает новую"""
        stmt = select(Job).where(
            Job.employee_id == employee_id,
            Job.employment_type_id == employment_type_id,
            Job.position_id == position_id,
            Job.division_id == division_id
        )
        result = await self.session.execute(stmt)
        job = result.scalars().first()

        if not job:
            job = Job(
                employee_id=employee_id,
                employment_type_id=employment_type_id,
                position_id=position_id,
                division_id=division_id,
                hire_date=hire_date,
                salary=salary
            )
            self.session.add(job)
            await self.session.commit()
            await self.session.refresh(job)

        return job
