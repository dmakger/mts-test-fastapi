from typing import Optional

from pydantic import BaseModel, Field


class BaseFilterSchema(BaseModel):
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)
    serialize: Optional[bool] = Field(False, description="Надо ли сериализировать")
