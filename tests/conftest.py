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
def sources(request):
    def construct_sources(contain_invalid=True):
        tmp_dir = f"tmp{os.urandom(4).hex()}"
        shutil.copytree("tests/data", tmp_dir)

        base_dir = tmp_dir + ("" if contain_invalid else "/valid")

        def fin():
            shutil.rmtree(tmp_dir)

        request.addfinalizer(fin)

        return base_dir, f"{tmp_dir}/valid/full.ghk", f"{tmp_dir}/valid/empty.ghk"

    return construct_sources
