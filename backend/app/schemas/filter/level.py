from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class LevelFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Level` из таблицы `levels`
    """
    name: Optional[str] = Field(None, min_length=1)
