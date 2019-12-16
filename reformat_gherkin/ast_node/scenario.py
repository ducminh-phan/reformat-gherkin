from itertools import chain
from typing import Optional, Tuple

from ._base import prepare
from .location import LocationMixin
from .step import Step
from .tag import Tag


@prepare
class Scenario(LocationMixin):
    keyword: str
    name: str
    steps: Tuple[Step, ...]
    tags: Tuple[Tag, ...]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)
