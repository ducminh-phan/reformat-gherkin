from .location import Location


class Feature:
    def __init__(
        self, language: str, location: Location, keyword: str, name: str, children
    ):
        self.language: str = language
        self.location: Location = location
        self.keyword: str = keyword
        self.name: str = name
        self.children = children
