from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from enum import Enum


class ReturnType(Enum):
    ALL = "all"
    FIRST = "first"
    LAST = "last"


class BaseService:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def find(self, filters: dict, return_type: ReturnType = ReturnType.ALL):
        """
        Универсальный метод поиска записей.

        :param filters: словарь с параметрами поиска (игнорируются None).
        :param return_type: ReturnType.ALL - все записи, ReturnType.FIRST - первая, ReturnType.LAST - последняя.
        :return: список, одна запись или None.
        """
        stmt = select(self.model)

        for key, value in filters.items():
            if value is not None:
                stmt = stmt.where(getattr(self.model, key) == value)

        if return_type == ReturnType.FIRST:
            result = await self.session.execute(stmt)
            return result.scalars().first()

        elif return_type == ReturnType.LAST:
            stmt = stmt.order_by(self.model.id.desc())
            result = await self.session.execute(stmt)
            return result.scalars().first()

        else:
            result = await self.session.execute(stmt)
            return result.scalars().all()

    async def update(self, item_id: int, updates: dict):
        """
        Универсальный метод обновления записей.
        """
        stmt = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(**updates)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def create(self, **data):
        """
        Создаёт новую запись в таблице.

        :param data: данные для создания записи.
        :return: созданная запись.
        """
        new_item = self.model(**data)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    async def get_or_create(self, defaults: dict, **filters):
        """
        Ищет запись по переданным фильтрам, если не найдена — создаёт.

        :param defaults: значения по умолчанию для создания.
        :param filters: параметры поиска.
        :return: найденная или созданная запись.
        """

        existing_item = await self.find(filters, return_type=ReturnType.FIRST)
        if existing_item:
            # print("QWE get_or_create get", existing_item, defaults, filters)
            return existing_item
        r = await self.create(**{**filters, **defaults})
        # print("QWE get_or_create create", r, defaults, filters)
        return r
