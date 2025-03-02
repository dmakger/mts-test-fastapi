from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema


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
