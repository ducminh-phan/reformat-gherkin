from unittest.mock import patch

import attr
import pytest

from reformat_gherkin import core
from reformat_gherkin.errors import (
    EquivalentError,
    InternalError,
    NothingChanged,
    StableError,
)
from tests.helpers import OPTIONS, dump_to_stderr, get_content


def test_assert_equivalent():
    login_content = get_content("login")
    login_equi_content = get_content("login_equi")

    core.assert_equivalent(login_content, login_equi_content)


@patch("reformat_gherkin.core.dump_to_file", dump_to_stderr)
def test_assert_equivalent_fail():
    login_content = get_content("login")
    login_no_equi_content = get_content("login_no_equi")

    with pytest.raises(EquivalentError):
        core.assert_equivalent(login_content, login_no_equi_content)


@patch("reformat_gherkin.core.dump_to_file", dump_to_stderr)
def test_assert_equivalent_invalid_dst(invalid_contents):
    login_content = get_content("login")
    invalid_content = next(invalid_contents)

    with pytest.raises(InternalError):
        core.assert_equivalent(login_content, invalid_content)


@pytest.mark.parametrize("options", OPTIONS)
def test_assert_stable(valid_contents, options):
    for content in valid_contents():
        formatted_content = core.format_file_contents(content, options=options)

        core.assert_stable(content, formatted_content, options=options)


@pytest.mark.parametrize("options", OPTIONS)
@patch("reformat_gherkin.core.dump_to_file", dump_to_stderr)
def test_assert_stable_fail(options):
    src = dst = get_content("full")

    with pytest.raises(StableError):
        core.assert_stable(src, dst, options=options)


def test_format_file_contents(valid_contents):
    for src, expected_dst, options in valid_contents(
        with_expected=True,
        with_options=True,
    ):
        dst = core.format_file_contents(src, options=options)

        for line in dst.splitlines():
            if line:
                assert line[-1] != " "

        assert dst == expected_dst


@pytest.mark.parametrize("options", OPTIONS)
def test_format_file_contents_no_change(options):
    with pytest.raises(NothingChanged):
        core.format_file_contents("", options=options)

    content = get_content("full")
    formatted_content = core.format_file_contents(content, options=options)

    with pytest.raises(NothingChanged):
        core.format_file_contents(formatted_content, options=options)


@pytest.mark.parametrize("newline_mode", core.NEWLINE_FROM_OPTION.keys())
@pytest.mark.parametrize("newline", core.NEWLINE_FROM_OPTION.values())
def test_line_separators_changed(source_with_newline, newline_mode, newline):
    options = OPTIONS[0]
    options = attr.evolve(
        options,
        write_back=core.WriteBackMode.INPLACE,
        newline=newline_mode,
    )

    source = source_with_newline(newline)

    core.reformat_single_file(source, options=options)

    with open(source, "rb") as buf:
        _newline = core.decode_stream(buf)[2]

        assert _newline == core.NEWLINE_FROM_OPTION[newline_mode]


@pytest.mark.parametrize("newline", core.NEWLINE_FROM_OPTION.values())
def test_line_separators_preserved(source_with_newline, newline):
    options = OPTIONS[0]
    options = attr.evolve(options, write_back=core.WriteBackMode.INPLACE)

    source = source_with_newline(newline)

    core.reformat_single_file(source, options=options)

    with open(source, "rb") as buf:
        _newline = core.decode_stream(buf)[2]

        assert _newline == newline


def test_format_comments():
    # This should be enough to exceed the maximum recursion depth
    number_of_comments = 1001

    dst = core.format_file_contents("#   \n" * number_of_comments, options=OPTIONS[0])
    assert dst == "#\n" * number_of_comments
