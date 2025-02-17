from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.level import Level


class LevelService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, name: str, level: int):
        """Ищет уровень или создает новый"""
        stmt = select(Level).where(
            Level.name == name,
            Level.level == level
        )
        result = await self.session.execute(stmt)
        level_obj = result.scalars().first()

        if not level_obj:
            level_obj = Level(name=name, level=level)
            self.session.add(level_obj)
            await self.session.commit()
            await self.session.refresh(level_obj)

        return level_obj
