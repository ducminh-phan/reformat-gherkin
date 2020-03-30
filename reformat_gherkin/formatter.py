from itertools import chain, groupby
from typing import Any, Dict, Iterator, List, Mapping, Optional, Set, Tuple, Union

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
    TagGroup,
)
from .options import AlignmentMode, TagLineMode
from .utils import camel_to_snake_case, extract_beginning_spaces, get_display_width

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
    step: Step,
    keyword_alignment: AlignmentMode,
    indent: str,
    *,
    keyword_padding_width: int = 0,
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
        step.keyword, keyword_alignment, keyword_padding_width=keyword_padding_width
    )

    return f"{indent * indent_level}{formatted_keyword} {step.text}"


def format_step_keyword(
    keyword: str, keyword_alignment: AlignmentMode, *, keyword_padding_width: int = 0
) -> str:
    """
    Insert padding to step keyword if necessary based on how we want to align them.
    """
    if keyword_alignment is AlignmentMode.NONE or keyword_padding_width <= 0:
        return keyword

    padding = " " * (keyword_padding_width - get_display_width(keyword))

    if keyword_alignment is AlignmentMode.LEFT:
        return keyword + padding
    else:
        return padding + keyword


def generate_keyword_line(
    keyword: str, name: str, indent: str, indent_level: int
) -> str:
    return f"{indent * indent_level}{keyword}: {name}".rstrip()


def generate_description_lines(
    description: Optional[str], indent: str, indent_level: int
) -> List[str]:
    description_lines = extract_description_lines(description)

    lines = [f"{indent * indent_level}{line}" for line in description_lines]

    # Add an empty line after the description, if it exists
    if lines:
        lines.append("")

    return lines


def extract_description_lines(description: Optional[str]) -> List[str]:
    if description is None:
        return []

    return description.splitlines()


def generate_table_lines(rows: List[TableRow], indent: str) -> List[str]:
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

    return [f"{indent * indent_level}{line}" for line in lines]


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


def generate_doc_string_lines(docstring: DocString, indent: str) -> List[str]:
    raw_lines = docstring.content.splitlines()
    raw_lines = ['"""'] + raw_lines + ['"""']

    indent_level = INDENT_LEVEL_MAP[Step]

    return [f"{indent * indent_level}{line}" for line in raw_lines]


ContextMap = Dict[Union[Comment, Tag, TagGroup, TableRow], Any]
Lines = Iterator[str]


@dataclass
class LineGenerator:
    ast: GherkinDocument
    step_keyword_alignment: AlignmentMode
    tag_line_mode: TagLineMode
    indent: str
    __nodes: List[Node] = attrib(init=False)
    __contexts: ContextMap = attrib(init=False)
    __nodes_with_newline: Set[Node] = attrib(init=False)
    __max_step_keyword_width: int = attrib(init=False)

    def __attrs_post_init__(self):
        # Use `__attrs_post_init__` instead of `property` to avoid re-computing attributes

        self.__nodes = list(self.ast)

        if self.tag_line_mode is TagLineMode.SINGLELINE:
            self.__group_tags()

        self.__nodes.sort(key=lambda node: node.location)

        self.__contexts = self.__construct_contexts()
        self.__nodes_with_newline = self.__find_nodes_with_newline()
        self.__max_step_keyword_width = self.__find_max_step_keyword_width()
        self.__add_language_header()

    def __group_tags(self):
        """
        Group the tags of a node, so that we can render them on a single line.
        """

        tag_groups: List[TagGroup] = []
        node: Node
        for node in self.ast:
            if hasattr(node, "tags"):
                tags: Tuple[Tag, ...] = node.tags

                if tags:
                    # The tag group should be placed at the position of the last tag
                    tag_group = TagGroup(
                        members=tags, context=node, location=tags[-1].location
                    )
                    tag_groups.append(tag_group)

        # After grouping the tags, we need to include the tag groups into
        # the list of nodes and remove the tags from the list.
        self.__nodes = [
            node for node in self.__nodes if not isinstance(node, Tag)
        ] + tag_groups

    def __construct_contexts(self) -> ContextMap:
        """
        Construct the information about the context a certain line might need to know to
        properly format these lines.
        """
        contexts: ContextMap = {}
        nodes = self.__nodes

        for node in nodes:
            if hasattr(node, "context"):
                contexts[node] = node.context  # type: ignore

            # We want tags to have the same indentation level with their parents
            for tag in getattr(node, "tags", []):
                contexts[tag] = node

            if isinstance(node, (DataTable, Examples)):
                # We need to know all rows in a table, so that the columns can be padded
                # to have the same widths across all rows. The context of a row is its
                # reformatted line.
                rows = extract_rows(node)
                lines = generate_table_lines(rows, self.indent)

                for row, line in zip(rows, lines):
                    contexts[row] = line

        contexts.update(self.__construct_contexts_for_comments(nodes))

        return contexts

    @staticmethod
    def __construct_contexts_for_comments(nodes: List[Node]) -> ContextMap:
        # The context of each comment line is the next non-comment line.
        #
        # The steps of the algorithm:
        # 1. Group the nodes into comments and non-comments
        # 2. The first node in each group of non-comments is the context of every node
        #    in the previous group, which consists of comments only.
        #
        # We start with a context of None, this lets us know if the document ends
        # with a block of comments.
        #
        # In the original algorithm, we simply set the context of each comment line
        # to be the next line. This leads to a RecursionError if there are too many
        # consecutive comments.

        contexts: ContextMap = {}
        current_context = None

        groups = groupby(reversed(nodes), lambda n: isinstance(n, Comment))

        for key, group in groups:
            if key is False:
                # The current group consists of non-comments, we set the current context
                # to be the last node in the group, since we grouped in the reverse order
                current_context = list(group)[-1]
            else:
                # The current group consists of comments. These comments should have the
                # same indent level, which is the indent level of the current context.
                for node in group:
                    contexts[node] = current_context  # type: ignore

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

    def __find_max_step_keyword_width(self) -> int:
        """
        Find the length of the longest step keyword in the document. This is
        used for aligning step keywords.
        """
        if self.step_keyword_alignment is AlignmentMode.NONE:
            # We don't need to align step keywords in this case.
            return 0

        step_keyword_widths = [
            get_display_width(node.keyword.strip())
            for node in self.ast
            if isinstance(node, Step)
        ]
        if not step_keyword_widths:
            return 0

        return max(step_keyword_widths)

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
        for node in self.__nodes:
            yield from self.visit(node)

            if node in self.__nodes_with_newline:
                yield ""

    def visit(self, node: Node) -> Lines:
        class_name = type(node).__name__

        yield from getattr(
            self, f"visit_{camel_to_snake_case(class_name)}", self.visit_default
        )(node)

    def visit_default(self, node: Node) -> Lines:
        indent_level = INDENT_LEVEL_MAP.get(type(node), 0)

        if hasattr(node, "keyword") and hasattr(node, "name"):
            yield generate_keyword_line(
                node.keyword, node.name, self.indent, indent_level  # type: ignore
            )

        if hasattr(node, "description"):
            yield from generate_description_lines(
                node.description, self.indent, indent_level + 1  # type: ignore
            )

    def visit_step(self, step: Step) -> Lines:
        yield generate_step_line(
            step,
            self.step_keyword_alignment,
            self.indent,
            keyword_padding_width=self.__max_step_keyword_width,
        )

    def visit_tag(self, tag: Tag) -> Lines:
        context = self.__contexts[tag]

        # Every node type containing tags is included in the indent map, so we don't
        # have to worry about KeyError here
        indent_level = INDENT_LEVEL_MAP[type(context)]

        yield f"{self.indent * indent_level}{tag.name}"

    def visit_tag_group(self, tag_group: TagGroup) -> Lines:
        context = self.__contexts[tag_group]

        indent_level = INDENT_LEVEL_MAP[type(context)]

        line_content = " ".join(tag.name for tag in tag_group.members)

        yield f"{self.indent * indent_level}{line_content}"

    def visit_table_row(self, row: TableRow) -> Lines:
        context = self.__contexts[row]

        yield context

    def visit_comment(self, comment: Comment) -> Lines:
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
            indent = self.indent * indent_level

        yield f"{indent}{comment.text}"

    def visit_doc_string(self, docstring: DocString) -> Lines:
        yield from generate_doc_string_lines(docstring, self.indent)
