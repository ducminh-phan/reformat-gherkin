from typing import List, Optional

from attr import dataclass

from .location import Location
from .step import Step


@dataclass(slots=True)
class Background:
    location: Location
    keyword: str
    name: str
    steps: List[Step]
    description: Optional[str] = None
