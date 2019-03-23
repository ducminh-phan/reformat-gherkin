from typing import List, Union

import attr

from .background import Background
from .location import Location
from .scenario import Scenario
from .scenario_outline import ScenarioOutline


@attr.s(slots=True, auto_attribs=True)
class Feature:
    language: str
    location: Location
    keyword: str
    name: str
    children: List[Union[Background, Scenario, ScenarioOutline]]
