from unittest.mock import patch

import pytest

from main import core
from main.errors import EquivalentError, InternalError
from tests.helpers import dump_to_stderr, get_content


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
