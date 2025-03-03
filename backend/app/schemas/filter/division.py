from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class DivisionFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Division` из таблицы `divisions`
    """
    name: Optional[str] = Field(None, min_length=1, description="Наименование подразделения")
    level_id: Optional[int] = Field(None, description="ID уровня")
    parent_id: Optional[int] = Field(None, description="ID родителя")
