from pydantic import BaseModel, ConfigDict

from . import LevelResponse


class PositionBaseResponse(BaseModel):
    """
    Базовая схема для модели `Position` из таблицы `positions`.
    """
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

class PositionResponse(PositionBaseResponse):
    """
    Схема ответа для модели `Position` из таблицы `positions`.
    """
    level_id: str


class PositionSerializerResponse(PositionBaseResponse):
    """
    Схема ответа для модели `Position` из таблицы `positions` с данными из связанных таблиц.
    Сериализированная модель. Каждый `FK` является объектом
    """
    level: LevelResponse
