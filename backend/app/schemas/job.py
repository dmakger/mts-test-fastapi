from datetime import date, datetime
from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema, EmployeeResponse


class JobFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `job` из таблицы `jobs`
    """
    serialize: Optional[bool] = Field(False, description="Надо ли сериализировать")
    employee_id: Optional[str] = Field(None, description="ID сотрудника")
    employment_type: Optional[int] = Field(None, description="ID типа занятости")
    position_id: Optional[int] = Field(None, description="ID должности")
    division_id: Optional[int] = Field(None, description="ID подразделения")
    head_id: Optional[int] = Field(None, description="ID руководителя")
    hire_date: Optional[date] = Field(None, description="Дата приёма на работу")
    dismissal_date: Optional[date] = Field(None, description="Дата увольнения")
    salary: Optional[float] = Field(None, ge=0, description="Зарплата")
    created_at: Optional[datetime] = Field(None, description="Дата создания записи")


# class JobResponse(BaseModel):
#     """
#     Схема ответа для модели `job` из таблицы `jobs` с данными из связанных таблиц
#     """
#     id: int = Field(..., description="ID записи о занятости")
#     employee_fio: str = Field(..., description="ФИО сотрудника")
#     employment_type: str = Field(..., description="Тип занятости")
#     position: str = Field(..., description="Название должности")
#     division: str = Field(..., description="Название подразделения")
#     head: Optional[str] = Field(None, description="ФИО руководителя")
#     hire_date: date = Field(..., description="Дата приёма на работу")
#     dismissal_date: Optional[date] = Field(None, description="Дата увольнения")
#     salary: float = Field(..., ge=0, description="Зарплата")
#     created_at: datetime = Field(..., description="Дата создания записи")
#
#     class Config:
#         from_attributes = True  # Для совместимости с SQLAlchemy


class JobSerializerResponse(BaseModel):
    """
    Схема ответа для модели `job` из таблицы `jobs` с данными из связанных таблиц.
    Сериализированная модель. Каждый `FK` является объектом
    """
    id: int = Field(..., description="ID записи о занятости")
    employee: EmployeeResponse = Field(..., description="ФИО сотрудника")
    employment_type: str = Field(..., description="Тип занятости")
    position: str = Field(..., description="Название должности")
    division: str = Field(..., description="Название подразделения")
    head: Optional[str] = Field(None, description="ФИО руководителя")
    hire_date: date = Field(..., description="Дата приёма на работу")
    dismissal_date: Optional[date] = Field(None, description="Дата увольнения")
    salary: float = Field(..., ge=0, description="Зарплата")
    created_at: datetime = Field(..., description="Дата создания записи")

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy