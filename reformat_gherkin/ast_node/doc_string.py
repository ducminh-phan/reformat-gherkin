from ._base import prepare
from .location import LocationMixin


@prepare
class DocString(LocationMixin):
    content: str

    def __iter__(self):
        yield self
