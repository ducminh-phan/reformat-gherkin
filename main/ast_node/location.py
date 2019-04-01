from attr import dataclass


@dataclass(slots=True)
class Location:
    line: int
    column: int
