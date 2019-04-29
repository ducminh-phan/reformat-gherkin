import os
import shutil
from glob import glob

import pytest


@pytest.fixture()
def valid_contents():
    def _valid_contents():
        for path in glob("tests/data/valid/*.feature"):
            with open(path, "r", encoding="utf-8") as f:
                yield f.read()

    return _valid_contents()


@pytest.fixture()
def invalid_contents():
    def _invalid_contents():
        for path in glob("tests/data/invalid/*.feature"):
            with open(path, "r", encoding="utf-8") as f:
                yield f.read()

    return _invalid_contents()


@pytest.fixture()
def sources():
    tmp_dir = f"tmp{os.urandom(4).hex()}"
    shutil.copytree("tests/data/valid", tmp_dir)

    yield tmp_dir, f"{tmp_dir}/full.ghk"

    shutil.rmtree(tmp_dir)
