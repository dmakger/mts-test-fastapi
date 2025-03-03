from pydantic import BaseModel, ConfigDict


class EmployeeBaseResponse(BaseModel):
    """
    Базовая схема для модели `Employee`, содержащая общие поля.
    """
    id: int
    fio: str

    model_config = ConfigDict(
        from_attributes=True
    )


class EmployeeResponse(EmployeeBaseResponse):
    """
    Схема для Ответа модели `employee` из таблицы `employees`
    """
    pass


class EmployeeSerializerResponse(EmployeeBaseResponse):
    """
    Схема для Ответа модели `employee` из таблицы `employees`
    Сериализированная модель. Каждый `FK` является объектом
    """
    pass
