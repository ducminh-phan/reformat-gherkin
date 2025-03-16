import textwrap
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from reformat_gherkin.utils import remove_trailing_spaces


class BaseNode(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        # The result keys from gherkin parser are in camelCase convention, for example,
        # tableHeader, tableBody.
        alias_generator=to_camel,
    )


def gherkin_string_validator(value: str) -> str:
    # For some types of node, the indentation of the lines is included
    # in the value of such nodes. Then the indentation can be changed after
    # formatting. Therefore, we need to dedent the value here for consistent
    # results. We also need to remove trailing spaces.

    value = remove_trailing_spaces(value)
    return textwrap.dedent(value)


GherkinString = Annotated[str, AfterValidator(gherkin_string_validator)]
