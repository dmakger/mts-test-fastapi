from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema


class JobLogFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `JobLog` из таблицы `job_logs`
    """
    job_id: Optional[int] = Field(None, description="ID job из `jobs`")
    column_name: Optional[str] = Field(None, description="Имя столбца")
    old_value: Optional[str] = Field(None, description="Старое значение")
    new_value: Optional[str] = Field(None, description="Новое значение")
    created_at: Optional[datetime] = Field(None, description="Дата создания записи")
