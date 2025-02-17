from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.employment_type import EmploymentType


class EmploymentTypeService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, name: str):
        """Ищет тип занятости или создает новый"""
        stmt = select(EmploymentType).where(
            EmploymentType.name == name
        )
        result = await self.session.execute(stmt)
        employment_type = result.scalars().first()

        if not employment_type:
            employment_type = EmploymentType(name=name)
            self.session.add(employment_type)
            await self.session.commit()
            await self.session.refresh(employment_type)

        return employment_type
