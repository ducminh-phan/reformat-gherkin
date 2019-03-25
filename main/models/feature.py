from typing import List, Optional, Union

import attr

from .background import Background
from .location import Location
from .scenario import Scenario
from .scenario_outline import ScenarioOutline
from .tag import Tag


@attr.s(slots=True, auto_attribs=True)
class Feature:
    language: str
    location: Location
    keyword: str
    name: str
    scenarios: List[Union[Scenario, ScenarioOutline]]
    tags: List[Tag]
    background: Optional[Background] = None
    description: Optional[str] = None
