from ._base import prepare


@prepare
class Location:
    line: int
    column: int
