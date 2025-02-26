from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema


class EmployeeFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `employee` из таблицы `employees`
    """
    fio: Optional[str] = Field(None, min_length=1)


class EmployeeResponse(BaseModel):
    """
    Схема для Ответа модели `employee` из таблицы `employees`
    """
    id: int
    fio: str

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy