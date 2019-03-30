from glob import glob

import pytest


@pytest.fixture(scope="session")
def valid_contents():
    for path in glob("tests/data/valid/*.feature"):
        with open(path, "r", encoding="utf-8") as f:
            yield f.read()


@pytest.fixture(scope="session")
def invalid_contents():
    def _invalid_contents():
        for path in glob("tests/data/invalid/*.feature"):
            with open(path, "r", encoding="utf-8") as f:
                yield f.read()

    return _invalid_contents()
