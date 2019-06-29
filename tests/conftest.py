import os
import shutil
from glob import iglob
from pathlib import Path

import pytest
from click.testing import CliRunner

from reformat_gherkin.config import CONFIG_FILE


@pytest.fixture()
def valid_contents():
    def _valid_contents(*, with_expected=False):
        for path_str in iglob("tests/data/valid/*.feature"):
            path = Path(path_str)

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

                if with_expected:
                    with open(
                        path.parents[1] / "expected" / path.name, "r", encoding="utf-8"
                    ) as ff:
                        expected_content = ff.read()

                    yield content, expected_content
                else:
                    yield content

    return _valid_contents


@pytest.fixture()
def invalid_contents():
    def _invalid_contents():
        for path in iglob("tests/data/invalid/*.feature"):
            with open(path, "r", encoding="utf-8") as f:
                yield f.read()

    return _invalid_contents()


@pytest.fixture()
def sources(request):
    def construct_sources(
        contain_invalid=True,
        with_config_file=False,
        valid_config=True,
        empty_config=False,
    ):
        tmp_dir = Path(f"tmp{os.urandom(4).hex()}")
        shutil.copytree("tests/data", tmp_dir)

        base_dir = tmp_dir
        if not contain_invalid:
            base_dir = tmp_dir / "valid"

        if with_config_file:
            file_name = "valid"
            if not valid_config:
                file_name = "invalid"
            if empty_config:
                file_name = "empty"

            shutil.copyfile(
                "tests/config_files/{}.yaml".format(file_name), tmp_dir / CONFIG_FILE
            )

        def fin():
            shutil.rmtree(tmp_dir)

        request.addfinalizer(fin)

        return (
            str(base_dir),
            str(tmp_dir / "valid" / "full.ghk"),
            str(tmp_dir / "valid" / "empty.ghk"),
        )

    return construct_sources


@pytest.fixture()
def runner():
    return CliRunner()
