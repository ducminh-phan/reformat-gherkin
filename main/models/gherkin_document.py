from typing import List

from .comment import Comment
from .feature import Feature


class GherkinDocument:
    def __init__(self, feature: Feature, comments: List[Comment]):
        self.feature: Feature = feature
        self.comments: List[Comment] = comments
