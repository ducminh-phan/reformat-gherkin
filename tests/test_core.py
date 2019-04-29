from unittest.mock import patch

import attr
import pytest

from main import core
from main.errors import EquivalentError, InternalError, NothingChanged, StableError
from main.report import Report
from tests.helpers import OPTIONS, dump_to_stderr, get_content


def test_assert_equivalent():
    login_content = get_content("login")
    login_equi_content = get_content("login_equi")

    core.assert_equivalent(login_content, login_equi_content)


@patch("main.core.dump_to_file", dump_to_stderr)
def test_assert_equivalent_fail():
    login_content = get_content("login")
    login_no_equi_content = get_content("login_no_equi")

    with pytest.raises(EquivalentError):
        core.assert_equivalent(login_content, login_no_equi_content)


@patch("main.core.dump_to_file", dump_to_stderr)
def test_assert_equivalent_invalid_dst(invalid_contents):
    login_content = get_content("login")
    invalid_content = next(invalid_contents)

    with pytest.raises(InternalError):
        core.assert_equivalent(login_content, invalid_content)


@pytest.mark.parametrize("options", OPTIONS)
def test_assert_stable(valid_contents, options):
    for content in valid_contents:
        formatted_content = core.format_file_contents(content, options=options)

        core.assert_stable(content, formatted_content, options=options)


@pytest.mark.parametrize("options", OPTIONS)
@patch("main.core.dump_to_file", dump_to_stderr)
def test_assert_stable_fail(options):
    src = dst = get_content("full")

    with pytest.raises(StableError):
        core.assert_stable(src, dst, options=options)


@pytest.mark.parametrize("options", OPTIONS)
def test_format_file_contents(valid_contents, options):
    for src in valid_contents:
        core.format_file_contents(src, options=options)


@pytest.mark.parametrize("options", OPTIONS)
def test_format_file_contents_no_change(options):
    with pytest.raises(NothingChanged):
        core.format_file_contents("", options=options)

    content = get_content("full")
    formatted_content = core.format_file_contents(content, options=options)

    with pytest.raises(NothingChanged):
        core.format_file_contents(formatted_content, options=options)


@pytest.mark.parametrize("check", [True, False])
@pytest.mark.parametrize("options", OPTIONS)
def test_reformat(sources, check, options):
    from main.options import WriteBackMode

    report = Report()
    options = attr.evolve(
        options, write_back=WriteBackMode.from_configuration(check=check)
    )

    core.reformat(sources, report, options=options)
