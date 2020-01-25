from attr import attrib

from ._base import prepare
from .location import LocationMixin


def escape_doc_string_value(text: str) -> str:
    """Escape triple-quotes in doc strings."""
    return text.replace('"""', '\\"\\"\\"')


@prepare
class DocString(LocationMixin):
    content: str = attrib(converter=escape_doc_string_value)

    def __iter__(self):
        yield self
