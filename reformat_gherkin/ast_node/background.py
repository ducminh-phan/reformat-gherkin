from itertools import chain
from typing import Tuple

from ._base import prepare
from .location import LocationMixin
from .step import Step


@prepare
class Background(LocationMixin):
    keyword: str
    name: str
    steps: Tuple[Step, ...]
    description: str

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
