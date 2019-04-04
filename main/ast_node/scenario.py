from itertools import chain
from typing import List, Optional

from attr import attrib

from ._base import prepare
from .location import Location
from .step import Step
from .tag import Tag


@prepare
class Scenario:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    name: str
    steps: List[Step]
    tags: List[Tag]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)
