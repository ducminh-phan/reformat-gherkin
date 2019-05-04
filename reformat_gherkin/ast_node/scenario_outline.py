from itertools import chain
from typing import Optional, Tuple

from attr import attrib

from ._base import prepare
from .examples import Examples
from .location import Location
from .step import Step
from .tag import Tag


@prepare
class ScenarioOutline:
    location: Location = attrib(cmp=False, repr=False)
    keyword: str
    name: str
    steps: Tuple[Step, ...]
    tags: Tuple[Tag, ...]
    examples: Tuple[Examples, ...]
    description: Optional[str] = None

    def __iter__(self):
        yield from self.tags

        yield self

        yield from chain.from_iterable(self.steps)

        yield from chain.from_iterable(self.examples)
