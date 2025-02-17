from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.position import Position


class PositionService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create(self, level_id: int, name: str):
        """Ищет позицию или создает новую"""
        stmt = select(Position).where(
            Position.level_id == level_id,
            Position.name == name
        )
        result = await self.session.execute(stmt)
        position = result.scalars().first()

        if not position:
            position = Position(level_id=level_id, name=name)
            self.session.add(position)
            await self.session.commit()
            await self.session.refresh(position)

        return position
