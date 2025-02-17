from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.division import Division


class DivisionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, level_id: int, parent_id: int, name: str,):
        """Ищет подразделение или создает новое"""
        stmt = select(Division).where(
            Division.level_id == level_id,
            Division.parent_id == parent_id,
            Division.name == name,
        )
        result = await self.session.execute(stmt)
        division = result.scalars().first()

        if not division:
            division = Division(
                level_id=level_id,
                parent_id=parent_id,
                name=name,
            )
            self.session.add(division)
            await self.session.commit()
            await self.session.refresh(division)

        return division
