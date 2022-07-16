import pytest

from reformat_gherkin import config


@pytest.mark.parametrize("vcs_dir", [".git", ".hg"])
def test_find_project_root_with_vcs(tmp_dir, vcs_dir):
    (tmp_dir / vcs_dir).mkdir(parents=True)

    src = tmp_dir / "a" / "b"
    src.mkdir(parents=True)

    root = config.find_project_root([str(src)])

    assert root.resolve() == tmp_dir.resolve()
