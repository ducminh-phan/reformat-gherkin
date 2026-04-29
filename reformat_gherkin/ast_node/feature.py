from itertools import chain

from ._base import DescriptionMixin, GherkinString, LocationMixin
from .rule import Rule, RuleChildren
from .tag import Tag


class FeatureChildren(RuleChildren):
    rule: Rule | None = None

    def __iter__(self):
        yield from super().__iter__()

        if self.rule is not None:
            yield from self.rule


class Feature(LocationMixin, DescriptionMixin):
    language: GherkinString
    keyword: GherkinString
    name: GherkinString
    children: tuple[FeatureChildren, ...]
    tags: tuple[Tag, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.children)
