from typing import Optional

from .data_table import DataTable
from .location import Location


class Step:
    def __init__(
        self,
        location: Location,
        keyword: str,
        text: str,
        argument: Optional[DataTable] = None,
    ):
        self.location: Location = location
        self.keyword: str = keyword
        self.text: str = text
        self.argument: Optional[DataTable] = argument
