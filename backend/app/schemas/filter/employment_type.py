from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class EmploymentTypeFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `EmploymentType` из таблицы `employment_types`
    """
    name: Optional[str] = Field(None, min_length=1)
