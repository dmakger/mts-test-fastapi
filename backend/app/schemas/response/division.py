from pydantic import BaseModel, ConfigDict

from . import LevelResponse


class DivisionBaseResponse(BaseModel):
    """
    Базовая схема для модели `Division` из таблицы `divisions`
    """
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class DivisionResponse(DivisionBaseResponse):
    """
    Схема для Ответа модели `Division` из таблицы `divisions`
    """
    level_id: int
    parent_id: int


class DivisionSerializerResponse(DivisionBaseResponse):
    """
    Схема для Ответа модели `Division` из таблицы `divisions`;
    Сериализированная модель. Каждый `FK` является объектом (кроме `parent_id`)
    """
    level: LevelResponse
    parent_id: int
