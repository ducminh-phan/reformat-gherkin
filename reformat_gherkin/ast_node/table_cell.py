from typing import Annotated

from pydantic import AfterValidator

from ._base import GherkinString, LocationMixin


def escape_table_cell_value(text: str) -> str:
    r"""
    Escape special characters in a table cell's value. There are three of them:
        - \\
        - \|
        - \n
    (Source: https://github.com/cucumber/common/blob/7cdd5259c90410971877dbe480733ba1b44e9a62/gherkin/testdata/good/escaped_pipes.feature)
    """

    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "\\n")


class TableCell(LocationMixin):
    value: Annotated[GherkinString, AfterValidator(escape_table_cell_value)]
