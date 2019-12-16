from ._base import prepare
from .location import LocationMixin


@prepare
class TableCell(LocationMixin):
    value: str
