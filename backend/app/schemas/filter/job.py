from datetime import date, datetime
from typing import Optional

from pydantic import Field

from . import BaseFilterSchema


class JobFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `Job` из таблицы `jobs`
    """
    employee_id: Optional[int] = Field(None, description="ID сотрудника")
    employment_type: Optional[int] = Field(None, description="ID типа занятости")
    position_id: Optional[int] = Field(None, description="ID должности")
    division_id: Optional[int] = Field(None, description="ID подразделения")
    head_id: Optional[int] = Field(None, description="ID руководителя")
    hire_date: Optional[date] = Field(None, description="Дата приёма на работу")
    dismissal_date: Optional[date] = Field(None, description="Дата увольнения")
    salary: Optional[float] = Field(None, ge=0, description="Зарплата")
    created_at: Optional[datetime] = Field(None, description="Дата создания записи")
