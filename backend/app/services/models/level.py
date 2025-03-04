from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import BaseService
from ...models import Level
from ...schemas import LevelBaseResponse, LevelResponse, LevelSerializerResponse

DEFAULT_LEVELS = [
    {"name": "Департамент", "level": 1},
    {"name": "Отдел", "level": 2},
]


class LevelService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Level)

    # ///====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======\\\
    def _to_base_response(self, item) -> LevelBaseResponse:
        return LevelBaseResponse.model_validate(item)

    def _to_basic_response(self, item) -> LevelResponse:
        base_response = self._to_base_response(item)
        return LevelResponse(**base_response.model_dump())

    def _to_serialized_response(self, item) -> LevelSerializerResponse:
        base_response = self._to_base_response(item)
        return LevelSerializerResponse(**base_response.model_dump())
    # \\\====={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }======///

    async def initialize_levels(self):
        """Добавляет начальные уровни, если они отсутствуют"""
        existing_levels = await self.session.execute(select(Level.name))
        existing_names = set(existing_levels.scalars())

        levels_to_add = [
            Level(**_level) for _level in DEFAULT_LEVELS if _level["name"] not in existing_names
        ]

        if levels_to_add:
            self.session.add_all(levels_to_add)
            await self.session.flush()
            await self.session.commit()

    async def get_default_levels(self) -> dict:
        """
        Возвращает ID дефолтных уровней из БД (или добавляет их, если их нет)
        :return: Словарь: Имя к Id записи
        """
        await self.initialize_levels()  # Убеждаемся, что уровни существуют

        result = await self.session.execute(select(Level.id, Level.name))
        levels = {name: level_id for level_id, name in result.all()}

        return levels
