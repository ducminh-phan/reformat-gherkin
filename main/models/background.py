from .location import Location


class Background:
    def __init__(self, location: Location, keyword: str, name: str, steps):
        self.location: Location = location
        self.keyword: str = keyword
        self.name: str = name
        self.steps = steps
