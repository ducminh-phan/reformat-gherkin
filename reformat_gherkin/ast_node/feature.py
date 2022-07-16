from itertools import chain
from typing import Optional, Tuple

from ._base import prepare
from .location import LocationMixin
from .rule import Rule, RuleChildren
from .tag import Tag


@prepare
class FeatureChildren(RuleChildren):
    rule: Optional[Rule] = None

    def __iter__(self):
        yield from super().__iter__()

        if self.rule is not None:
            yield from self.rule


@prepare
class Feature(LocationMixin):
    language: str
    keyword: str
    name: str
    children: Tuple[FeatureChildren, ...]
    tags: Tuple[Tag, ...]
    description: str

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
