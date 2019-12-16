from ._base import prepare
from .location import LocationMixin


@prepare
class Tag(LocationMixin):
    name: str
