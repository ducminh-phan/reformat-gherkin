from itertools import chain

from ._base import BaseNode, DescriptionMixin, GherkinString, LocationMixin
from .background import Background
from .scenario import Scenario
from .tag import Tag


class RuleChildren(BaseNode):
    background: Background | None = None
    scenario: Scenario | None = None

    def __iter__(self):
        if self.background is not None:
            yield from self.background

        if self.scenario is not None:
            yield from self.scenario


class Rule(LocationMixin, DescriptionMixin):
    keyword: GherkinString
    name: GherkinString
    tags: tuple[Tag, ...]
    children: tuple[RuleChildren, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
