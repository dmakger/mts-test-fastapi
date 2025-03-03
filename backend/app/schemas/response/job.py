from datetime import date, datetime
from typing import Optional

from pydantic import Field, BaseModel, ConfigDict

from . import EmployeeResponse, EmploymentTypeResponse, PositionSerializerResponse, \
    DivisionSerializerResponse


class JobBaseResponse(BaseModel):
    """
    Базовая схема для модели `Job`, содержащая общие поля.
    """
    id: int = Field(..., description="ID записи о занятости")
    hire_date: date = Field(..., description="Дата приёма на работу")
    dismissal_date: Optional[date] = Field(None, description="Дата увольнения")
    salary: float = Field(..., ge=0, description="Зарплата")
    created_at: datetime = Field(..., description="Дата создания записи")

    model_config = ConfigDict(
        from_attributes=True
    )

class JobResponse(JobBaseResponse):
    """
    Схема ответа для модели `Job` из таблицы `jobs`
    """
    employee_id: int = Field(..., description="ID сотрудника")
    employment_type_id: int = Field(..., description="ID типа занятости")
    position_id: int = Field(..., description="Название должности")
    division_id: int = Field(..., description="Название подразделения")
    head_id: Optional[int] = Field(None, description="ФИО руководителя")


class JobSerializerResponse(JobBaseResponse):
    """
    Схема ответа для модели `Job` из таблицы `jobs` с данными из связанных таблиц.
    Сериализированная модель. Каждый `FK` является объектом
    """
    employee: EmployeeResponse = Field(..., description="ФИО сотрудника")
    employment_type: EmploymentTypeResponse = Field(..., description="Тип занятости")
    position: PositionSerializerResponse = Field(..., description="Название должности")
    division: DivisionSerializerResponse = Field(..., description="Название подразделения")
    head: Optional[EmployeeResponse] = Field(None, description="ФИО руководителя")
