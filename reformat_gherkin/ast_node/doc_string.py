from typing import Annotated

from pydantic import AfterValidator

from ._base import GherkinString
from .location import LocationMixin


def escape_doc_string_value(text: str) -> str:
    """Escape triple-quotes in doc strings."""
    return text.replace('"""', '\\"\\"\\"')


class DocString(LocationMixin):
    content: Annotated[GherkinString, AfterValidator(escape_doc_string_value)]
    media_type: GherkinString = ""

    def __iter__(self):
        yield self
