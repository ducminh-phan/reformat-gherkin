from .location import Location


class Comment:
    def __init__(self, location: Location, text: str):
        self.location: Location = location
        self.text: str = text
