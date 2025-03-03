from pydantic import BaseModel, ConfigDict


class EmploymentTypeBaseResponse(BaseModel):
    """
    Базовая схема для модели `EmploymentType` из таблицы `employment_types`
    """
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class EmploymentTypeResponse(EmploymentTypeBaseResponse):
    """
    Схема для Ответа модели `EmploymentType` из таблицы `employment_types`
    """
    pass


class EmploymentTypeSerializerResponse(EmploymentTypeBaseResponse):
    """
    Схема для Ответа модели `EmploymentType` из таблицы `employment_types`
    Сериализированная модель. Каждый `FK` является объектом
    """
    pass
