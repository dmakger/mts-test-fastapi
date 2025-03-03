from datetime import datetime

from pydantic import Field, BaseModel, ConfigDict

from . import JobSerializerResponse


class JobLogBaseResponse(BaseModel):
    """
    Базовая схема для модели `JobLog` из таблицы `job_logs`;
    """
    id: int = Field(..., description="ID записи о занятости")
    column_name: str = Field(..., description="Имя столбца")
    old_value: str = Field(..., description="Старое значение")
    new_value: str = Field(..., description="Новое значение")
    created_at: datetime = Field(..., description="Дата создания записи")

    model_config = ConfigDict(
        from_attributes=True
    )

class JobLogResponse(JobLogBaseResponse):
    """
    Схема ответа для модели `JobLog` из таблицы `job_logs`;
    """
    job_id: str = Field(..., description="ID `job` из `jobs`")


class JobLogSerializeResponse(JobLogBaseResponse):
    """
    Схема ответа для модели `JobLog` из таблицы `job_logs`;
    Сериализированная модель. Каждый `FK` является объектом
    """
    job: JobSerializerResponse = Field(..., description="Модель `job` из `jobs`")
