from itertools import chain
from typing import Optional

from ._base import BaseNode, GherkinString
from .background import Background
from .location import LocationMixin
from .scenario import Scenario
from .tag import Tag


class RuleChildren(BaseNode):
    background: Optional[Background] = None
    scenario: Optional[Scenario] = None

    def __iter__(self):
        if self.background is not None:
            yield from self.background

        if self.scenario is not None:
            yield from self.scenario


class Rule(LocationMixin):
    keyword: GherkinString
    name: GherkinString
    tags: tuple[Tag, ...]
    children: tuple[RuleChildren, ...]
    description: GherkinString

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
