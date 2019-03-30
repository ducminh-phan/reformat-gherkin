from typing import List, Optional

from attr import attrib, dataclass

from .examples import Examples
from .location import Location
from .step import Step
from .tag import Tag


@dataclass(slots=True)
class ScenarioOutline:
    location: Location = attrib(cmp=False)
    keyword: str
    name: str
    steps: List[Step]
    tags: List[Tag]
    examples: List[Examples]
    description: Optional[str] = None
