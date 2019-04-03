from typing import Union

from .background import Background
from .comment import Comment
from .data_table import DataTable
from .examples import Examples
from .feature import Feature
from .gherkin_document import GherkinDocument
from .location import Location
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .step import Step
from .table_cell import TableCell
from .table_row import TableRow
from .tag import Tag

Node = Union[
    Background,
    Comment,
    DataTable,
    Examples,
    Feature,
    GherkinDocument,
    Location,
    Scenario,
    ScenarioOutline,
    Step,
    TableCell,
    TableRow,
    Tag,
]
