from attr import attrib

from ._base import prepare
from .location import LocationMixin


def escape_table_cell_value(text: str) -> str:
    r"""
    Escape special characters in a table cell's value. There are three of them:
        - \\
        - \|
        - \n
    (Source: https://github.com/cucumber/common/blob/7cdd5259c90410971877dbe480733ba1b44e9a62/gherkin/testdata/good/escaped_pipes.feature)
    """

    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "\\n")


@prepare
class TableCell(LocationMixin):
    value: str = attrib(converter=escape_table_cell_value)
