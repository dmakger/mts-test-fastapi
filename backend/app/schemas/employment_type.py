from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema


class EmploymentTypeFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `EmploymentType` из таблицы `employment_types`
    """
    name: Optional[str] = Field(None, min_length=1)


class EmploymentTypeResponse(BaseModel):
    """
    Схема для Ответа модели `EmploymentType` из таблицы `employment_types`
    """
    id: int
    name: str

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy