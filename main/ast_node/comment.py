from attr import attrib, dataclass

from .location import Location


@dataclass(slots=True)
class Comment:
    location: Location = attrib(cmp=False, repr=False)
    text: str
