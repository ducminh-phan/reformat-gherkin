from typing import Optional, Tuple

from ._base import prepare
from .comment import Comment
from .feature import Feature


@prepare
class GherkinDocument:
    comments: Tuple[Comment, ...]
    feature: Optional[Feature] = None

    def __iter__(self):
        yield from self.comments

        if self.feature is not None:
            yield from self.feature
