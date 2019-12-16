from itertools import chain
from typing import Optional, Tuple

from ._base import prepare
from .location import LocationMixin
from .step import Step


@prepare
class Background(LocationMixin):
    keyword: str
    name: str
    steps: Tuple[Step, ...]
    description: Optional[str] = None

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
