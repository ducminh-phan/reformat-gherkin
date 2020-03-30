import os
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from reformat_gherkin.config import CONFIG_FILE
from tests.helpers import FILENAME_OPTION_MAP

TEST_DIR = Path("tests")


@pytest.fixture
def valid_contents():
    def _valid_contents(*, with_expected=False, with_options=False):
        for feature_dir in (TEST_DIR / "data" / "valid").iterdir():
            if not feature_dir.is_dir():
                continue
            content = (feature_dir / "input.feature").read_text(encoding="utf-8")
            for expected in feature_dir.glob("expected_*.feature"):
                result = [content]
                if with_expected:
                    result.append(expected.read_text(encoding="utf-8"))
                if with_options:
                    options = FILENAME_OPTION_MAP[expected.stem]
                    result.append(options)
                if len(result) <= 1:
                    yield result[0]
                else:
                    yield tuple(result)

    return _valid_contents


@pytest.fixture
def invalid_contents():
    def _invalid_contents():
        for path in (TEST_DIR / "data" / "invalid").rglob("*.feature"):
            yield path.read_text(encoding="utf-8")

    return _invalid_contents()


@pytest.fixture
def sources(request):
    # noinspection PyTypeChecker
    def construct_sources(
        contain_invalid=True,
        with_config_file=False,
        valid_config=True,
        empty_config=False,
    ):
        tmp_dir = Path(f"tmp{os.urandom(4).hex()}")
        tmp_dir.mkdir()

        for valid_dir in (TEST_DIR / "data" / "valid").iterdir():
            if valid_dir.is_dir():
                shutil.copyfile(
                    valid_dir / "input.feature", tmp_dir / f"{valid_dir.name}.feature"
                )
            else:
                shutil.copyfile(valid_dir, tmp_dir / valid_dir.name)

        if contain_invalid:
            for invalid_feature in (TEST_DIR / "data" / "invalid").rglob("*.feature"):
                shutil.copyfile(invalid_feature, tmp_dir / invalid_feature.name)

        if with_config_file:
            file_name = "valid"
            if not valid_config:
                file_name = "invalid"
            if empty_config:
                file_name = "empty"

            shutil.copyfile(
                TEST_DIR / "config_files" / "{}.yaml".format(file_name),
                tmp_dir / CONFIG_FILE,
            )

        def fin():
            shutil.rmtree(tmp_dir)

        request.addfinalizer(fin)

        return str(tmp_dir), str(tmp_dir / "full.ghk"), str(tmp_dir / "empty.ghk")

    return construct_sources


@pytest.fixture
def source_with_newline(request):
    def construct_source_with_newline(newline):
        tmp_file = Path(f"tmp{os.urandom(4).hex()}.feature")

        content = (TEST_DIR / "data" / "valid" / "full" / "input.feature").read_text(
            encoding="utf-8"
        )
        with tmp_file.open("w", newline=newline) as f:
            f.write(content)

        def fin():
            tmp_file.unlink()

        request.addfinalizer(fin)

        return tmp_file

    return construct_source_with_newline


@pytest.fixture
def runner():
    return CliRunner()
