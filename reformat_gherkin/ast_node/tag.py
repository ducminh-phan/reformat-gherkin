from ._base import GherkinString, LocationMixin


class Tag(LocationMixin):
    name: GherkinString
