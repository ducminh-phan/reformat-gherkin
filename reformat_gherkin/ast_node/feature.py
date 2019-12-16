from itertools import chain
from typing import Optional, Tuple, Union

from ._base import prepare
from .background import Background
from .location import LocationMixin
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .tag import Tag


@prepare
class Feature(LocationMixin):
    language: str
    keyword: str
    name: str
    children: Tuple[Union[Background, Scenario, ScenarioOutline], ...]
    tags: Tuple[Tag, ...]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
