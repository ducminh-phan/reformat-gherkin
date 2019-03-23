from typing import List

import attr

from .location import Location
from .step import Step
from .tag import Tag


@attr.s(slots=True, auto_attribs=True)
class Scenario:
    location: Location
    keyword: str
    name: str
    steps: List[Step]
    tags: List[Tag]
