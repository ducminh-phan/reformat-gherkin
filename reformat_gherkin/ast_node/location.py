from pydantic import Field
from pydantic.dataclasses import dataclass

from ._base import BaseNode


@dataclass(frozen=True, eq=True, order=True)
class Location:
    line: int
    column: int


class LocationMixin(BaseNode):
    # The location field should be excluded from model serialization for AST diff
    location: Location = Field(exclude=True)
