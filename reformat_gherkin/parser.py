import io
from typing import TypeVar

from gherkin.errors import ParserError
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from .ast_node.gherkin_document import GherkinDocument
from .errors import DeserializeError, InvalidInput


T = TypeVar("T")


# noinspection PyMissingConstructor
class StringOnlyTokenScanner(TokenScanner):
    """
    A replacement for Gherkin's TokenScanner that doesn't load from files.

    This is necessary to prevent "path too long for Windows" errors when Windows
    treats large feature files as paths on the file system (bug #34).
    """

    def __init__(self, content):
        self.io = io.StringIO(content)
        self.line_number = 0


def parse(content: str) -> GherkinDocument:
    """
    Parse the content of a file to an AST.
    """
    parser = Parser()

    try:
        parse_result = parser.parse(StringOnlyTokenScanner(content))
    except ParserError as e:
        raise InvalidInput(e) from e

    try:
        result = GherkinDocument.model_validate(parse_result)
    except Exception as e:
        raise DeserializeError(f"{type(e).__name__}: {e}") from e

    return result
