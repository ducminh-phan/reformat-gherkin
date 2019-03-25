from typing import List, Optional

import attr

from .comment import Comment
from .feature import Feature


@attr.s(slots=True, auto_attribs=True)
class GherkinDocument:
    comments: List[Comment]
    feature: Optional[Feature] = None
