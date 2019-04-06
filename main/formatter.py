from functools import lru_cache
from itertools import zip_longest
from typing import Any, Dict, Iterator, List, Optional, Union

from attr import attrib, dataclass

from .ast_node import (
    Background,
    Comment,
    DataTable,
    Examples,
    Feature,
    GherkinDocument,
    Node,
    Scenario,
    ScenarioOutline,
    Step,
    TableRow,
    Tag,
)
from .options import AlignmentMode
from .utils import camel_to_snake_case, extract_beginning_spaces, get_step_keywords

INDENT = "  "
INDENT_LEVEL_MAP = {
    Feature: 0,
    Background: 1,
    Scenario: 1,
    ScenarioOutline: 1,
    Step: 2,
    Examples: 2,
    TableRow: 3,
}


def generate_step_line(
    step: Step,
    keyword_alignment: AlignmentMode,
    *,
    indent_level: int = INDENT_LEVEL_MAP[Step],
    dialect_name: str = "en",
) -> str:
    """
    Generate lines for steps. The step keywords are aligned according to the parameter
    `keyword_alignment`. For example:

    If `keyword_alignment = AlignmentMode.NONE`:
        Given Enter search term 'Cucumber'
        When Do search
        Then Single result is shown for 'Cucumber'

    If `keyword_alignment = AlignmentMode.LEFT`:
        Given Enter search term 'Cucumber'
        When  Do search
        Then  Single result is shown for 'Cucumber'

    If `keyword_alignment = AlignmentMode.Right`:
        Given Enter search term 'Cucumber'
         When Do search
         Then Single result is shown for 'Cucumber'
    """
    formatted_keyword = format_step_keyword(
        step.keyword, keyword_alignment, dialect_name=dialect_name
    )

    return f"{INDENT * indent_level}{formatted_keyword} {step.text}"


def format_step_keyword(
    keyword: str, keyword_alignment: AlignmentMode, *, dialect_name: str = "en"
) -> str:
    """
    Insert padding to step keyword if necessary based on how we want to align them.
    """
    keyword = keyword.strip()

    if keyword_alignment is AlignmentMode.NONE:
        return keyword

    all_keywords = get_step_keywords(dialect_name)
    max_keyword_length = max(map(len, all_keywords))
    padding = " " * (max_keyword_length - len(keyword))

    if keyword_alignment is AlignmentMode.LEFT:
        return keyword + padding
    else:
        return padding + keyword


def generate_keyword_line(keyword: str, name: str, indent_level: int) -> str:
    return f"{INDENT * indent_level}{keyword}: {name}"


def generate_description_lines(
    description: Optional[str], indent_level: int
) -> List[str]:
    description_lines = extract_description_lines(description)

    return [f"{INDENT * indent_level}{line}" for line in description_lines]


def extract_description_lines(description: Optional[str]) -> List[str]:
    if description is None:
        return []

    lines = description.splitlines()

    return [line.strip() for line in lines]


def generate_table_lines(rows: List[TableRow]) -> List[str]:
    """
    Generate lines for table. The columns in a table need to have the same width.
    """
    if not rows:
        return []

    indent_level = INDENT_LEVEL_MAP[TableRow]

    n_columns = len(rows[0])

    # Find the max width of a cell in a column, so that every cell in the same column
    # has the same width
    column_widths = [
        max(len(row[column_index].value) for row in rows)
        for column_index in range(n_columns)
    ]

    lines = []
    for row in rows:
        line = "|"

        for column_index in range(n_columns):
            # Left-align the content of each cell, fix the width of the cell
            line += f" {row[column_index].value:<{column_widths[column_index]}} |"

        lines.append(line)

    return [f"{INDENT * indent_level}{line}" for line in lines]


def extract_rows(node: Union[DataTable, Examples]) -> List[TableRow]:
    """
    Extract table rows from either a Datable or Example instance.
    """
    if isinstance(node, DataTable):
        return list(node.rows)

    rows = []

    if isinstance(node, Examples):
        header = node.table_header
        body = node.table_body

        if header is not None:
            rows.append(header)

        if body is not None:
            rows.extend(body)

    return rows


ContextMap = Dict[Union[Comment, Tag, TableRow], Any]


@dataclass(cmp=False)
class LineGenerator:
    ast: GherkinDocument
    step_keyword_alignment: AlignmentMode
    nodes: List[Node] = attrib(init=False)
    __contexts: ContextMap = attrib(init=False)

    def __attrs_post_init__(self):
        """
        Use `__attrs_post_init__` instead of `property` to avoid re-computing attributes
        """
        self.nodes = sorted(list(self.ast), key=lambda node: node.location)
        self.__contexts = self.__construct_contexts()

    def __construct_contexts(self) -> ContextMap:
        """
        Construct the information about the context a certain line might need to know to
        properly format these lines.
        """
        contexts: ContextMap = {}
        nodes = self.nodes

        for node in nodes:
            # We want tags to have the same indentation level with their parents
            for tag in getattr(node, "tags", []):
                contexts[tag] = node

            if isinstance(node, (DataTable, Examples)):
                # We need to know all rows in a table, so that the columns can be padded
                # to have the same widths across all rows. The context of a row is its
                # reformatted line.
                rows = extract_rows(node)
                lines = generate_table_lines(rows)

                for row, line in zip(rows, lines):
                    contexts[row] = line

        for node, next_node in zip_longest(nodes, nodes[1:], fillvalue=None):
            if isinstance(node, Comment):
                # We want comments to have the same indentation level with the next line
                contexts[node] = next_node

        return contexts

    def generate(self) -> Iterator[str]:
        for node in self.nodes:
            yield from self.visit(node)

    @lru_cache()
    def visit(self, node: Node) -> Iterator[str]:
        class_name = type(node).__name__

        yield from getattr(
            self, f"visit_{camel_to_snake_case(class_name)}", self.visit_default
        )(node)

    @staticmethod
    def visit_default(node: Node) -> Iterator[str]:
        indent_level = INDENT_LEVEL_MAP.get(type(node), 0)

        if hasattr(node, "keyword") and hasattr(node, "name"):
            yield generate_keyword_line(
                node.keyword, node.name, indent_level  # type: ignore
            )

        if hasattr(node, "description"):
            yield from generate_description_lines(
                node.description, indent_level + 1  # type: ignore
            )

    def visit_gherkin_document(self, document: GherkinDocument) -> Iterator[str]:
        yield from self.visit(document.feature)

    def visit_step(self, step: Step) -> Iterator[str]:
        yield generate_step_line(step, self.step_keyword_alignment)

    def visit_tag(self, tag: Tag):
        context = self.__contexts[tag]

        # Every node type containing tags is included in the indent map, so we don't
        # have to worry about KeyError here
        indent_level = INDENT_LEVEL_MAP[type(context)]

        yield f"{INDENT * indent_level}{tag.name}"

    def visit_table_row(self, row: TableRow):
        context = self.__contexts[row]

        yield context

    def visit_comment(self, comment: Comment):
        context = self.__contexts[comment]

        # Find the indent level of this comment line
        if context is None:
            # In this case, this comment line is the last line of the document
            indent_level: Optional[int] = 0
        else:
            # Try to look for the indent level of the context in the mapping. If not
            # successful, then we use the same amount of white spaces to indent as
            # the next line.
            indent_level = INDENT_LEVEL_MAP.get(type(context))

        if indent_level is None:
            next_line = next(self.visit(context))
            indent = extract_beginning_spaces(next_line)
        else:
            indent = INDENT * indent_level

        yield f"{indent}{comment.text.strip()}"
