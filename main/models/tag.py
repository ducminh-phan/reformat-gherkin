from .location import Location


class Tag:
    def __init__(self, location: Location, name: str):
        self.location: Location = location
        self.name: str = name
