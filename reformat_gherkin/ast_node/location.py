from ._base import prepare


@prepare(eq=True)
class Location:
    line: int
    column: int
