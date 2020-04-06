import io
import textwrap
from typing import Any, Dict, Type, TypeVar

from cattr.converters import Converter
from gherkin.errors import ParserError
from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from .ast_node.gherkin_document import GherkinDocument
from .errors import DeserializeError, InvalidInput
from .utils import camel_to_snake_case, remove_trailing_spaces

T = TypeVar("T")


class CustomConverter(Converter):
    def structure_attrs_fromdict(self, obj: Dict[str, Any], cls: Type[T]) -> T:
        # Make sure the type in the parsed object matches the class we use
        # to structure the object
        if "type" in obj:
            type_name = obj.pop("type")
            cls_name = cls.__name__
            assert type_name == cls_name, f"{type_name} does not match {cls_name}"

        # Note that keys are in camelCase convention, for example, tableHeader,
        # tableBody. Therefore, we need to convert the keys to snake_case.
        transformed_obj = {}
        for key, value in obj.items():
            if isinstance(value, str):
                # For some types of node, the indentation of the lines is included
                # in the value of such nodes. Then the indentation can be changed after
                # formatting. Therefore, we need to dedent the value here for consistent
                # results. We also need to remove trailing spaces.
                value = remove_trailing_spaces(value)
                value = textwrap.dedent(value)

            transformed_obj[camel_to_snake_case(key)] = value

        return super(CustomConverter, self).structure_attrs_fromdict(
            transformed_obj, cls
        )


converter = CustomConverter()


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
        result = converter.structure(parse_result, GherkinDocument)
    except Exception as e:
        raise DeserializeError(f"{type(e).__name__}: {e}") from e

    return result
