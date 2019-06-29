import os
import shutil
from pathlib import Path

import pytest

from reformat_gherkin import config


@pytest.mark.parametrize("vcs_dir", [".git", ".hg"])
def test_find_project_root_with_vcs(vcs_dir):
    tmp_dir = Path(f"tmp{os.urandom(4).hex()}")
    os.makedirs(tmp_dir / vcs_dir)

    src = tmp_dir / "a" / "b"
    os.makedirs(src)

    root = config.find_project_root([src])

    assert root.resolve() == tmp_dir.resolve()

    shutil.rmtree(tmp_dir)
