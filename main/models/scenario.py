from typing import List, Optional

from attr import dataclass

from .location import Location
from .step import Step
from .tag import Tag


@dataclass(slots=True)
class Scenario:
    location: Location
    keyword: str
    name: str
    steps: List[Step]
    tags: List[Tag]
    description: Optional[str] = None
