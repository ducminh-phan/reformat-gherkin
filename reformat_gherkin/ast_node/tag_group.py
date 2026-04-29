from ._base import LocationMixin
from .examples import Examples
from .feature import Feature
from .rule import Rule
from .scenario import Scenario
from .tag import Tag


class TagGroup(LocationMixin):
    members: tuple[Tag, ...]
    context: Examples | Feature | Scenario | Rule
