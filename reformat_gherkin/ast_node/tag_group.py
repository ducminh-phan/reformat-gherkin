from typing import Union

from .examples import Examples
from .feature import Feature
from .location import LocationMixin
from .rule import Rule
from .scenario import Scenario
from .tag import Tag


class TagGroup(LocationMixin):
    members: tuple[Tag, ...]
    context: Union[Examples, Feature, Scenario, Rule]
