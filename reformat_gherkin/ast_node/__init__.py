from typing import Union

from .background import Background
from .comment import Comment
from .data_table import DataTable
from .doc_string import DocString
from .examples import Examples
from .feature import Feature
from .gherkin_document import GherkinDocument
from .location import Location
from .rule import Rule
from .scenario import Scenario
from .step import Step
from .table_cell import TableCell
from .table_row import TableRow
from .tag import Tag
from .tag_group import TagGroup

Node = Union[
    Background,
    Comment,
    DataTable,
    DocString,
    Examples,
    Feature,
    GherkinDocument,
    Location,
    Rule,
    Scenario,
    Step,
    TableCell,
    TableRow,
    Tag,
    TagGroup,
]
