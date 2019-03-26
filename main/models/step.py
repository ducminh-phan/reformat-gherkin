from typing import Optional

from attr import dataclass

from .data_table import DataTable
from .location import Location


@dataclass(slots=True)
class Step:
    location: Location
    keyword: str
    text: str
    argument: Optional[DataTable] = None
