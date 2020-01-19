from typing import Tuple, Union

from ._base import prepare
from .examples import Examples
from .feature import Feature
from .location import LocationMixin
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .tag import Tag


@prepare
class TagGroup(LocationMixin):
    members: Tuple[Tag, ...]
    context: Union[Examples, Feature, Scenario, ScenarioOutline]
