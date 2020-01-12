from itertools import chain
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, Set, Union

from attr import attrib, dataclass

from .ast_node import (
    Background,
    Comment,
    DataTable,
    DocString,
    Examples,
    Feature,
    GherkinDocument,
    Location,
    Node,
    Scenario,
    ScenarioOutline,
    Step,
    TableRow,
    Tag,
)
from .options import AlignmentMode, TagLineMode
from .utils import camel_to_snake_case, get_display_width, get_step_keywords

INDENT = "  "
INDENT_LEVEL_MAP: Mapping[Any, int] = {
    Feature: 0,
    Background: 1,
    Scenario: 1,
    ScenarioOutline: 1,
    Step: 2,
    Examples: 2,
    TableRow: 3,
}


def generate_language_header(language: str) -> Comment:
    return Comment(Location(1, 1), f"# language: {language}")  # type: ignore


def generate_step_line(
    step: Step, keyword_alignment: AlignmentMode, *, dialect_name: str = "en"
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
    indent_level: int = INDENT_LEVEL_MAP[Step]

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
    return f"{INDENT * indent_level}{keyword}: {name}".rstrip()


def generate_description_lines(
    description: Optional[str], indent_level: int
) -> List[str]:
    description_lines = extract_description_lines(description)

    lines = [f"{INDENT * indent_level}{line}" for line in description_lines]

    # Add an empty line after the description, if it exists
    if lines:
        lines.append("")

    return lines


def extract_description_lines(description: Optional[str]) -> List[str]:
    if description is None:
        return []

    return description.splitlines()


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
        max(get_display_width(row[column_index].value) for row in rows)
        for column_index in range(n_columns)
    ]

    lines = []
    for row in rows:
        line = "|"

        for column_index in range(n_columns):
            # Left-align the content of each cell, fix the width of the cell
            content = row[column_index].value
            column_width = column_widths[column_index]
            content_width = get_display_width(content)
            padding = " " * (column_width - content_width)
            line += f" {content}{padding} |"

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


def generate_doc_string_lines(docstring: DocString) -> List[str]:
    raw_lines = docstring.content.splitlines()
    raw_lines = ['"""'] + raw_lines + ['"""']

    indent_level = INDENT_LEVEL_MAP[Step]

    return [f"{INDENT * indent_level}{line}" for line in raw_lines]


ContextMap = Dict[Union[Comment, Tag, TableRow], Any]
Lines = Iterator[str]


@dataclass
class LineGenerator:
    ast: GherkinDocument
    step_keyword_alignment: AlignmentMode
    tag_line_mode: TagLineMode
    __nodes: List[Node] = attrib(init=False)
    __contexts: ContextMap = attrib(init=False)
    __nodes_with_newline: Set[Node] = attrib(init=False)

    def __attrs_post_init__(self):
        # Use `__attrs_post_init__` instead of `property` to avoid re-computing attributes
        self.__nodes = sorted(list(self.ast), key=lambda node: node.location)
        self.__contexts = self.__construct_contexts()
        self.__nodes_with_newline = self.__find_nodes_with_newline()
        self.__add_language_header()

    def __construct_contexts(self) -> ContextMap:
        """
        Construct the information about the context a certain line might need to know to
        properly format these lines.
        """
        contexts: ContextMap = {}
        comment_parent = None

        for node in reversed(self.__nodes):
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

            if isinstance(node, Comment):
                # We want comments to have the same indentation level as the nearest
                # node that has an entry in the indent level map.
                contexts[node] = comment_parent
            elif type(node) in INDENT_LEVEL_MAP:
                comment_parent = node

        return contexts

    def __find_nodes_with_newline(self) -> Set[Node]:
        """
        Find all nodes in the AST that needs a new line after it.
        """
        nodes_with_newline: Set[Node] = set()

        node: Optional[Node] = None

        for node in self.__nodes:
            # We want to add a newline after the Feature line, even if it does not
            # have a description. If the feature has a description, we already add
            # a newline after each description.
            if isinstance(node, Feature) and node.description is None:
                nodes_with_newline.add(node)

            children: List[Node] = []

            # Add an empty line after the last step, including its argument, if any
            if isinstance(node, (Background, Scenario, ScenarioOutline)):
                children = list(chain.from_iterable(node.steps))

            # Add an empty line after an examples table
            if isinstance(node, Examples):
                children = list(node)

            if children:
                last_child = children[-1]
                nodes_with_newline.add(last_child)

        # Add the last node in the AST so that we have an empty line at the end
        if node is not None:
            nodes_with_newline.add(node)

        return nodes_with_newline

    def __add_language_header(self) -> None:
        """Add a language header if the Feature language is not English."""
        # Exit if the language is English or if there is no Feature node
        feature = self.ast.feature
        if not feature:
            return
        language = feature.language
        if language == "en":
            return

        # Register the language header
        language_header = generate_language_header(language)
        self.__nodes.insert(0, language_header)
        self.__nodes_with_newline.add(language_header)
        self.__contexts[language_header] = self.ast.feature

    def generate(self) -> Lines:
        i = 0
        while i < len(self.__nodes):
            node = self.__nodes[i]
            if isinstance(node, (Tag, Comment)):
                # We need to treat comments and tags specially; if we are using
                # TagLineMode.SINGLELINE then we might only yield one line for
                # several tag nodes, and the order of the tags and comments may
                # change.
                comments_and_tags = []
                for node in self.__nodes[i:]:
                    if isinstance(node, (Tag, Comment)):
                        comments_and_tags.append(node)
                        i += 1
                    else:
                        break
                yield from self.generate_comment_and_tag_lines(comments_and_tags)
            else:
                yield from self.visit(node)
                i += 1

    def visit(self, node: Node) -> Lines:
        class_name = type(node).__name__

        yield from getattr(
            self, f"visit_{camel_to_snake_case(class_name)}", self.visit_default
        )(node)
        if node in self.__nodes_with_newline:
            yield ""

    @staticmethod
    def visit_default(node: Node) -> Lines:
        indent_level = INDENT_LEVEL_MAP.get(type(node), 0)

        if hasattr(node, "keyword") and hasattr(node, "name"):
            yield generate_keyword_line(
                node.keyword, node.name, indent_level  # type: ignore
            )

        if hasattr(node, "description"):
            yield from generate_description_lines(
                node.description, indent_level + 1  # type: ignore
            )

    def visit_step(self, step: Step) -> Lines:
        yield generate_step_line(step, self.step_keyword_alignment)

    def visit_tag(self, tag: Tag) -> Lines:
        context = self.__contexts[tag]

        # Every node type containing tags is included in the indent map, so we don't
        # have to worry about KeyError here
        indent_level = INDENT_LEVEL_MAP[type(context)]

        yield f"{INDENT * indent_level}{tag.name}"

    def visit_comment(self, comment: Comment) -> Lines:
        context = self.__contexts[comment]

        # Find the indent level of this comment line
        if context is None:
            # In this case, this comment line at the end of the document
            indent_level = 0
        else:
            # Look up the indent level of the context in the indent level map.
            # All contexts for comments have an entry in the map, so we don't
            # have to worry about KeyError here.
            indent_level = INDENT_LEVEL_MAP[type(context)]

        yield f"{INDENT * indent_level}{comment.text}"

    def visit_table_row(self, row: TableRow) -> Lines:
        context = self.__contexts[row]

        yield context

    @staticmethod
    def visit_doc_string(docstring: DocString) -> Lines:
        yield from generate_doc_string_lines(docstring)

    def generate_comment_and_tag_lines(
        self, comments_and_tags: Sequence[Union[Comment, Tag]]
    ):
        if self.tag_line_mode == TagLineMode.MULTILINE:
            for node in comments_and_tags:
                yield from self.visit(node)
        else:
            # For single-line tags, the order of the tags and comments can be
            # switched. For example:
            #
            #   # Comment 1
            #   @tag1 @tag2
            #   # Comment 2
            #   @tag3
            #   # Comment 3
            #
            # is rendered as:
            #
            #   # Comment 1
            #   # Comment 2
            #   @tag1 @tag2 @tag3
            #   # Comment 3
            #
            # To enable reordering, we split our input nodes into three
            # categories: comments that go before the tags, the tags, and
            # comments that go after the tags. Once we have separated the nodes,
            # we then render each of the categories in turn.
            comments_before: List[Comment] = []
            tags: List[Tag] = []
            comments_after: List[Comment] = []
            for node in reversed(comments_and_tags):
                if isinstance(node, Comment):
                    if tags:
                        comments_before.append(node)
                    else:
                        comments_after.append(node)
                else:
                    tags.append(node)

            for comment in reversed(comments_before):
                yield from self.visit(comment)
            if tags:
                context = self.__contexts[tags[0]]
                indent_level = INDENT_LEVEL_MAP[type(context)]
                yield f"{INDENT * indent_level}" + " ".join(
                    tag.name for tag in reversed(tags)
                )
            for comment in reversed(comments_after):
                yield from self.visit(comment)
