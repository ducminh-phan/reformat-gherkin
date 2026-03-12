from itertools import chain

from ._base import DescriptionMixin, GherkinString, LocationMixin
from .step import Step


class Background(LocationMixin, DescriptionMixin):
    keyword: GherkinString
    name: GherkinString
    steps: tuple[Step, ...]

    def __iter__(self):
        yield self

        yield from chain.from_iterable(self.steps)
