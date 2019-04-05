from ._base import prepare


@prepare(cmp=True)
class Location:
    line: int
    column: int
