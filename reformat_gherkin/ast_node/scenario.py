from itertools import chain

from ._base import GherkinString
from .examples import Examples
from .location import LocationMixin
from .step import Step
from .tag import Tag


class Scenario(LocationMixin):
    keyword: GherkinString
    name: GherkinString
    steps: tuple[Step, ...]
    tags: tuple[Tag, ...]
    description: GherkinString
    examples: tuple[Examples, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)

        yield from chain.from_iterable(self.examples)
