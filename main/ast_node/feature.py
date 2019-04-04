from itertools import chain
from typing import Optional, Tuple, Union

from attr import attrib

from ._base import prepare
from .background import Background
from .location import Location
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .tag import Tag


@prepare
class Feature:
    language: str
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    name: str
    children: Tuple[Union[Background, Scenario, ScenarioOutline], ...]
    tags: Tuple[Tag, ...]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
