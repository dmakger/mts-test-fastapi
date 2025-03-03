from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema, LevelResponse


class DivisionFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Division` из таблицы `divisions`
    """
    name: Optional[str] = Field(None, min_length=1, description="Наименование подразделения")
    level_id: Optional[int] = Field(None, description="ID уровня")
    parent_id: Optional[int] = Field(None, description="ID родителя")


class DivisionResponse(BaseModel):
    """
    Схема для Ответа модели `Division` из таблицы `divisions`
    """
    id: int
    name: str
    level_id: int
    parent_id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy


class DivisionSerializerResponse(BaseModel):
    """
    Схема для Ответа модели `Division` из таблицы `divisions`;
    Сериализированная модель. Каждый `FK` является объектом (кроме `parent_id`)
    """
    id: int
    name: str
    level: LevelResponse
    parent_id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy