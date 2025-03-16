from itertools import chain
from typing import Optional

from ._base import GherkinString
from .location import LocationMixin
from .rule import Rule, RuleChildren
from .tag import Tag


class FeatureChildren(RuleChildren):
    rule: Optional[Rule] = None

    def __iter__(self):
        yield from super().__iter__()

        if self.rule is not None:
            yield from self.rule


class Feature(LocationMixin):
    language: GherkinString
    keyword: GherkinString
    name: GherkinString
    children: tuple[FeatureChildren, ...]
    tags: tuple[Tag, ...]
    description: GherkinString

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
