from .location import Location


class TableCell:
    def __init__(self, location: Location, value: str):
        self.location: Location = location
        self.value: str = value
