from typing import List, Optional

import attr

from .location import Location
from .step import Step


@attr.s(slots=True, auto_attribs=True)
class Background:
    location: Location
    keyword: str
    name: str
    steps: List[Step]
    description: Optional[str] = None
