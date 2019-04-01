from itertools import chain
from typing import List, Optional, Union

from attr import attrib, dataclass

from .background import Background
from .location import Location
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .tag import Tag


@dataclass(slots=True)
class Feature:
    language: str
    location: Location = attrib(cmp=False)
    keyword: str
    name: str
    children: List[Union[Background, Scenario, ScenarioOutline]]
    tags: List[Tag]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
