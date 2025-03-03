from typing import TypeVar, Union, Dict, List

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import joinedload

from . import ReturnType, ResponseFormat, with_response_format

# Тип для схемы фильтрации
FilterType = TypeVar("FilterType", bound=BaseModel)


class BaseService:
    # Список связанных полей, которые нужно догружать (будет переопределяться в наследниках)
    relationships: List = []

    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    # ========={ ОБЯЗАТЕЛЬНЫЕ ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ }=========

    def _to_base_response(self, item):
        """Возвращает базовые данные объекта. Переопределяется в дочерних классах."""
        raise NotImplementedError("Method '_get_base_data' must be implemented in subclass")

    def _to_basic_response(self, item):
        """Преобразует объект в базовый формат ответа."""
        raise NotImplementedError("Method '_to_basic_response' must be implemented in subclass")

    def _to_serialized_response(self, item):
        """Преобразует объект в сериализованный формат ответа."""
        raise NotImplementedError("Method '_to_serialized_response' must be implemented in subclass")

    def _to_response(self, item, response_format: ResponseFormat):
        """
        Преобразует объект модели в схему ответа.

        :param item: объект модели (например, Job)
        :param response_format: формат ответа (NONE, RAW, BASIC, SERIALIZED)
        :return: объект Pydantic-схемы (например, JobResponse или JobSerializerResponse или Raw)
        """
        print("GOL _to_response", response_format)

        if response_format == ResponseFormat.RAW:
            return item
        elif response_format == ResponseFormat.SERIALIZED:
            return self._to_serialized_response(item)
        return self._to_basic_response(item)

    # ========={ ОБЩИЕ }=========

    @with_response_format
    async def find(
            self,
            filters: Union[FilterType, Dict],
            return_type: ReturnType = ReturnType.ALL,
            response_format: ResponseFormat = ResponseFormat.RAW,
    ):
        """
        Универсальный метод поиска записей с фильтрацией.

        :param filters: объект Pydantic или словарь с параметрами.
        :param return_type: ReturnType.ALL - все записи, ReturnType.FIRST - первая, ReturnType.LAST - последняя.
        :param response_format: формат ответа (NONE, RAW, BASIC, SERIALIZED). Необходим для `@with_response_format`
        :return: список, одна запись или None.
        """
        # Если передан объект Pydantic, превращаем в словарь
        if isinstance(filters, BaseModel):
            filters = filters.model_dump(exclude_unset=True)

        stmt = select(self.model).limit(filters.get('limit', 10)).offset(filters.get('offset', 0))
        if response_format == ResponseFormat.SERIALIZED and self.relationships:
            stmt = stmt.options(*[joinedload(rel) for rel in self.relationships])

        for key, value in filters.items():
            if key not in ('limit', 'offset', 'serialize') and value is not None:
                stmt = stmt.where(getattr(self.model, key) == value)

        if return_type == ReturnType.FIRST:
            result = await self.session.execute(stmt)
            return result.scalars().first()
        elif return_type == ReturnType.LAST:
            stmt = stmt.order_by(self.model.id.desc())
            result = await self.session.execute(stmt)
            return result.scalars().first()
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, item_id: int, updates: dict, response_format: ResponseFormat = ResponseFormat.BASIC):
        """
        Универсальный метод обновления записей.

        :param updates:
        :param item_id:
        :param response_format: формат ответа (NONE, RAW, BASIC, SERIALIZED). Необходим для `.find`
        """
        stmt = (
            update(self.model)
            .where(self.model.id == item_id)
            .values(**updates)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        if response_format != ResponseFormat.NONE:
            return await self.find({"id": item_id}, return_type=ReturnType.FIRST, response_format=response_format)

    @with_response_format
    async def create(self, response_format: ResponseFormat = ResponseFormat.BASIC, **data):
        """
        Создаёт новую запись в таблице.

        :param response_format: формат ответа (NONE, RAW, BASIC, SERIALIZED). Необходим для `@with_response_format`
        :param data: данные для создания записи.
        :return: созданная запись.
        """
        new_item = self.model(**data)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item

    @with_response_format
    async def get_or_create(
            self,
            defaults: dict,
            response_format: ResponseFormat = ResponseFormat.RAW,
            **filters
    ):
        """
        Ищет запись по переданным фильтрам, если не найдена — создаёт.

        :param response_format: значение
        :param defaults: значения по умолчанию для создания.
        :param response_format: формат ответа (RAW, BASIC, SERIALIZED). Необходим для `@with_response_format`
        :param filters: параметры поиска.
        :return: найденная или созданная запись.
        """

        existing_item = await self.find(filters, return_type=ReturnType.FIRST)
        if existing_item:
            # print("QWE get_or_create get", existing_item, defaults, filters)
            return existing_item
        r = await self.create(**{**filters, **defaults})
        return r
