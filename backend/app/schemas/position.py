from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema, LevelResponse


class PositionFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Position` из таблицы `positions`
    """
    level_id: Optional[int] = Field(None)
    name: Optional[str] = Field(None, min_length=1)


class PositionResponse(BaseModel):
    """
    Схема для Ответа модели `employee` из таблицы `employees`
    """
    id: int
    level_id: str
    name: str

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy


class PositionSerializerResponse(BaseModel):
    """
    Схема ответа для модели `Position` из таблицы `positions` с данными из связанных таблиц.
    Сериализированная модель. Каждый `FK` является объектом
    """
    id: int
    level: LevelResponse
    name: str

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy

