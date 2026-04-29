from ._base import BaseNode
from .comment import Comment
from .feature import Feature


class GherkinDocument(BaseNode):
    comments: tuple[Comment, ...]
    feature: Feature | None = None

    def __iter__(self):
        yield from self.comments

        if self.feature is not None:
            yield from self.feature
