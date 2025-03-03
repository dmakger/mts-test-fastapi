from datetime import date, datetime
from typing import Optional

from pydantic import Field, BaseModel

from . import BaseFilterSchema, EmployeeResponse, JobSerializerResponse


class JobLogFilterSchema(BaseFilterSchema):
    """
    Фильтры для сущности `JobLog` из таблицы `job_logs`
    """
    job_id: Optional[int] = Field(None, description="ID job из `jobs`")
    column_name: Optional[str] = Field(None, description="Имя столбца")
    old_value: Optional[str] = Field(None, description="Старое значение")
    new_value: Optional[str] = Field(None, description="Новое значение")
    created_at: Optional[datetime] = Field(None, description="Дата создания записи")


class JobLogResponse(BaseModel):
    """
    Схема ответа для модели `JobLog` из таблицы `job_logs`;
    """
    id: int = Field(..., description="ID записи о занятости")
    job_id: str = Field(..., description="ID job из `jobs`")
    column_name: str = Field(..., description="Имя столбца")
    old_value: str = Field(..., description="Старое значение")
    new_value: str = Field(..., description="Новое значение")
    created_at: datetime = Field(..., description="Дата создания записи")

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy


class JobLogSerializeResponse(BaseModel):
    """
    Схема ответа для модели `JobLog` из таблицы `job_logs`;
    Сериализированная модель. Каждый `FK` является объектом
    """
    id: int = Field(..., description="ID записи о занятости")
    job: JobSerializerResponse = Field(..., description="ID job из `jobs`")
    column_name: str = Field(..., description="Имя столбца")
    old_value: str = Field(..., description="Старое значение")
    new_value: str = Field(..., description="Новое значение")
    created_at: datetime = Field(..., description="Дата создания записи")

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy
