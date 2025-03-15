from typing import Union

from ._base import prepare
from .examples import Examples
from .feature import Feature
from .location import LocationMixin
from .scenario import Scenario
from .tag import Tag


@prepare
class TagGroup(LocationMixin):
    members: tuple[Tag, ...]
    context: Union[Examples, Feature, Scenario]
