from typing import List

from .location import Location
from .tag import Tag


class ScenarioOutline:
    def __init__(
        self,
        location: Location,
        keyword: str,
        name: str,
        steps,
        tags: List[Tag],
        examples,
    ):
        self.location: Location = location
        self.keyword: str = keyword
        self.name: str = name
        self.steps = steps
        self.tags: List[Tag] = tags
        self.examples = examples
