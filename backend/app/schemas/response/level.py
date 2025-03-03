from pydantic import BaseModel, ConfigDict


class LevelBaseResponse(BaseModel):
    """
    Базовая схема для модели `Level` из таблицы `levels`
    """
    id: int
    name: str
    level: int

    model_config = ConfigDict(
        from_attributes=True
    )


class LevelResponse(LevelBaseResponse):
    """
    Схема для Ответа модели `Level` из таблицы `levels`
    """
    pass


class LevelSerializerResponse(LevelBaseResponse):
    """
    Схема для Ответа модели `Level` из таблицы `levels`
    Сериализированная модель. Каждый `FK` является объектом
    """
    pass
