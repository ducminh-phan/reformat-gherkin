from itertools import chain
from typing import Tuple

from ._base import prepare
from .examples import Examples
from .location import LocationMixin
from .step import Step
from .tag import Tag


@prepare
class Scenario(LocationMixin):
    keyword: str
    name: str
    steps: Tuple[Step, ...]
    tags: Tuple[Tag, ...]
    description: str
    examples: Tuple[Examples, ...]

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)

        yield from chain.from_iterable(self.examples)
