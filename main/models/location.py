import attr


@attr.s(slots=True, auto_attribs=True)
class Location:
    line: int = attr.ib()
    column: int = attr.ib()
