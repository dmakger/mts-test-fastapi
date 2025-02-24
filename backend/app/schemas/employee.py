from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class EmployeeFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `employee` из таблицы `employees`
    """
    fio: Optional[str] = Field(None, min_length=1)
