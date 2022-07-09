import secrets
import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from reformat_gherkin.config import CONFIG_FILE
from tests.helpers import FILENAME_OPTION_MAP

TEST_DIR = Path("tests")
VALID_DATA_DIR = TEST_DIR / "data" / "valid"
INVALID_DATA_DIR = TEST_DIR / "data" / "invalid"


@pytest.fixture
def valid_contents():
    def _valid_contents(*, with_expected=False, with_options=False):
        for feature_dir in VALID_DATA_DIR.iterdir():
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
        for path in INVALID_DATA_DIR.rglob("*.feature"):
            yield path.read_text(encoding="utf-8")

    return _invalid_contents()


@pytest.fixture
def tmp_dir():
    _tmp_dir = Path(f"tmp_{secrets.token_hex(4)}")
    _tmp_dir.mkdir()

    return _tmp_dir


@pytest.fixture
def sources(request, tmp_dir):
    def construct_sources(
        contain_invalid=True,
        with_config_file=False,
        valid_config=True,
        empty_config=False,
    ):
        for feature_dir in VALID_DATA_DIR.iterdir():
            if feature_dir.is_dir():
                shutil.copyfile(
                    feature_dir / "input.feature",
                    tmp_dir / f"{feature_dir.name}.feature",
                )
            else:
                shutil.copyfile(
                    feature_dir,
                    tmp_dir / feature_dir.name,
                )

        if contain_invalid:
            for invalid_feature in INVALID_DATA_DIR.rglob("*.feature"):
                shutil.copyfile(
                    invalid_feature,
                    tmp_dir / invalid_feature.name,
                )

        if with_config_file:
            file_name = "valid"
            if not valid_config:
                file_name = "invalid"
            if empty_config:
                file_name = "empty"

            shutil.copyfile(
                TEST_DIR / "config_files" / f"{file_name}.yaml",
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
        tmp_file = Path(f"tmp_{secrets.token_hex(4)}.feature")

        content = (VALID_DATA_DIR / "full" / "input.feature").read_text(
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
    return CliRunner(mix_stderr=False)
