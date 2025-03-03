from enum import Enum
from functools import wraps
from typing import Callable


class ReturnType(Enum):
    """
    Возвращаемый тип
    """
    ALL = "all"
    FIRST = "first"
    LAST = "last"


class ResponseFormat(Enum):
    """
    Формат возврата
    """
    NONE = "none"  # Ничего не возвращает
    RAW = "raw"  # Без преобразования, возвращает объект модели
    BASIC = "basic"  # Преобразование в базовый Response
    SERIALIZED = "serialized"  # Преобразование в SerializerResponse


def with_response_format(func: Callable):
    """
    Декоратор, который обрабатывает результат метода в указанный формат ответа.
    """
    @wraps(func)
    async def wrapper(self, *args, response_format: ResponseFormat = ResponseFormat.BASIC, **kwargs):
        print("PPPP with_response_format", response_format, args, kwargs)
        if response_format == ResponseFormat.NONE:
            return None
        result = await func(self, *args, **kwargs)
        if result is None:
            return None
        if isinstance(result, list):
            return [self._to_response(item, response_format) for item in result]
        return self._to_response(result, response_format)

    return wrapper
