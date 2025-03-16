import textwrap
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic.dataclasses import dataclass

from reformat_gherkin.utils import remove_trailing_spaces


class BaseNode(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        # The result keys from gherkin parser are in camelCase convention, for example,
        # tableHeader, tableBody.
        alias_generator=to_camel,
    )


@dataclass(frozen=True, eq=True, order=True)
class Location:
    line: int
    column: int


class LocationMixin(BaseNode):
    # The location field should be excluded from model serialization for AST diff
    location: Location = Field(exclude=True)


def gherkin_string_validator(value: str) -> str:
    # For some types of node, the indentation of the lines is included
    # in the value of such nodes. Then the indentation can be changed after
    # formatting. Therefore, we need to dedent the value here for consistent
    # results. We also need to remove trailing spaces.

    value = remove_trailing_spaces(value)
    return textwrap.dedent(value)


GherkinString = Annotated[str, AfterValidator(gherkin_string_validator)]

GherkinDescription = Annotated[GherkinString, AfterValidator(str.rstrip)]


class DescriptionMixin(BaseNode):
    description: GherkinDescription
