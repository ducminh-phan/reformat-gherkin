from itertools import chain

from ._base import DescriptionMixin, GherkinString, LocationMixin
from .examples import Examples
from .step import Step
from .tag import Tag


class Scenario(LocationMixin, DescriptionMixin):
    keyword: GherkinString
    name: GherkinString
    steps: tuple[Step, ...]
    tags: tuple[Tag, ...]
    examples: tuple[Examples, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)

        yield from chain.from_iterable(self.examples)
