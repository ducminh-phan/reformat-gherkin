import pytest

from reformat_gherkin.errors import DeserializeError, InvalidInput
from reformat_gherkin.parser import parse


def test_invalid_input(invalid_contents):
    for content in invalid_contents:
        with pytest.raises(InvalidInput):
            parse(content)


def test_valid_input(valid_contents):
    for content in valid_contents():
        parse(content)


def test_parse_with_exception(mocker, valid_contents):
    exception_message = "exception message"
    mocker.patch(
        "reformat_gherkin.parser.converter.structure",
        side_effect=Exception(exception_message),
    )

    for content in valid_contents():
        with pytest.raises(DeserializeError) as exc_info:
            parse(content)

        assert exception_message in str(exc_info.value)
