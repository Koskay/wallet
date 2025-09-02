from typing import (
    Any,
    Generic,
    TypeVar,
)

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


TData = TypeVar("TData")


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)


class CamelCaseSchema(BaseModel):

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )