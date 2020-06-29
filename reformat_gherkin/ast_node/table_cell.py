from attr import attrib

from ._base import prepare
from .location import LocationMixin


def escape_table_cell_value(text: str) -> str:
    """
    Escape pipe characters `|` in a table cell's value. Since the pipe characters
    are used to separate cells in a row, we need to replace them by `\\|`.
    """

    return text.replace("|", "\\|").replace('\\\"', '\\\\\"')


@prepare
class TableCell(LocationMixin):
    value: str = attrib(converter=escape_table_cell_value)
