from itertools import chain
from typing import Optional, Tuple

from ._base import prepare
from .background import Background
from .location import LocationMixin
from .scenario import Scenario
from .tag import Tag


@prepare
class RuleChildren:
    background: Optional[Background] = None
    scenario: Optional[Scenario] = None

    def __iter__(self):
        if self.background is not None:
            yield from self.background

        if self.scenario is not None:
            yield from self.scenario


@prepare
class Rule(LocationMixin):
    keyword: str
    name: str
    tags: Tuple[Tag, ...]
    children: Tuple[RuleChildren, ...]
    description: str

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
