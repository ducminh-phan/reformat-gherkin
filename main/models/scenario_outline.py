from typing import List, Optional

import attr

from .examples import Examples
from .location import Location
from .step import Step
from .tag import Tag


@attr.s(slots=True, auto_attribs=True)
class ScenarioOutline:
    location: Location
    keyword: str
    name: str
    steps: List[Step]
    tags: List[Tag]
    examples: List[Examples]
    description: Optional[str]
