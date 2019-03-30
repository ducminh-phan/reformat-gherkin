from typing import Optional

from attr import attrib, dataclass

from .data_table import DataTable
from .location import Location


@dataclass(slots=True)
class Step:
    location: Location = attrib(cmp=False)
    keyword: str
    text: str
    argument: Optional[DataTable] = None
