from itertools import chain

from ._base import GherkinString
from .location import LocationMixin
from .step import Step


class Background(LocationMixin):
    keyword: GherkinString
    name: GherkinString
    steps: tuple[Step, ...]
    description: GherkinString

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
