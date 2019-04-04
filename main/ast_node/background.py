from itertools import chain
from typing import List, Optional

from attr import attrib

from ._base import prepare
from .location import Location
from .step import Step


@prepare
class Background:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    name: str
    steps: List[Step]
    description: Optional[str] = None

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
