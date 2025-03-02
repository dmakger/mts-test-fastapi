from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema


class LevelFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Level` из таблицы `levels`
    """
    name: Optional[str] = Field(None, min_length=1)


class LevelResponse(BaseModel):
    """
    Схема для Ответа модели `Level` из таблицы `levels`
    """
    id: int
    name: str
    level: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy
