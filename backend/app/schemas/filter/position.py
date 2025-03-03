from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class PositionFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Position` из таблицы `positions`
    """
    level_id: Optional[int] = Field(None)
    name: Optional[str] = Field(None, min_length=1)
