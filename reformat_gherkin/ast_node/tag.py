from ._base import GherkinString
from .location import LocationMixin


class Tag(LocationMixin):
    name: GherkinString
