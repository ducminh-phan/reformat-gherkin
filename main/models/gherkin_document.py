from typing import List

import attr

from .comment import Comment
from .feature import Feature


@attr.s(slots=True, auto_attribs=True)
class GherkinDocument:
    feature: Feature
    comments: List[Comment]
