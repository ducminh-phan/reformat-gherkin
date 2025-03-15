from itertools import chain

from ._base import prepare
from .examples import Examples
from .location import LocationMixin
from .step import Step
from .tag import Tag


@prepare
class Scenario(LocationMixin):
    keyword: str
    name: str
    steps: tuple[Step, ...]
    tags: tuple[Tag, ...]
    description: str
    examples: tuple[Examples, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)

        yield from chain.from_iterable(self.examples)
