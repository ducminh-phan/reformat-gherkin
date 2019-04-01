from itertools import chain
from typing import List, Optional

from attr import attrib, dataclass

from .location import Location
from .step import Step


@dataclass(slots=True)
class Background:
    location: Location = attrib(cmp=False)
    keyword: str
    name: str
    steps: List[Step]
    description: Optional[str] = None

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
