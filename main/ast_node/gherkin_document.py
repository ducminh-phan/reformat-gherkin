from typing import List, Optional

from ._base import prepare
from .comment import Comment
from .feature import Feature


@prepare
class GherkinDocument:
    comments: List[Comment]
    feature: Optional[Feature] = None

    def __iter__(self):
        yield from self.comments

        if self.feature is not None:
            yield from self.feature
