import hashlib
import shutil
import subprocess
import tempfile
from collections.abc import Iterable
from pathlib import Path

import tomli


GHERKIN_TEST_DATA_DIR = Path("tests/gherkin_test_data")


def get_test_data_files(dir_path: Path) -> Iterable[Path]:
    return dir_path.glob("*.feature")


def compute_hash(paths: Iterable[Path]) -> str:
    h = hashlib.sha3_512()
    for path in paths:
        h.update(path.read_bytes())

    return h.hexdigest()


def get_gherkin_tag() -> str:
    with open("pyproject.toml", "rb") as f:
        pyproject_data = tomli.load(f)

    version = pyproject_data["tool"]["poetry"]["dependencies"]["gherkin-official"]
    return f"v{version}"


def prepare_data():
    gherkin_tag = get_gherkin_tag()

    with tempfile.TemporaryDirectory() as tmp_dir:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth=1",
                f"--branch={gherkin_tag}",
                "https://github.com/cucumber/gherkin",
                tmp_dir,
            ],
        )

        origin_test_data_dir = Path(tmp_dir) / "testdata" / "good"
        origin_hash = compute_hash(get_test_data_files(origin_test_data_dir))
        current_hash = compute_hash(get_test_data_files(GHERKIN_TEST_DATA_DIR))

        if origin_hash == current_hash:
            print("Content hash does not change. Exiting...")
            return

        print("Removing current test data files...")
        for file in get_test_data_files(GHERKIN_TEST_DATA_DIR):
            file.unlink()

        print("Copying origin test data files...")
        for file in get_test_data_files(origin_test_data_dir):
            shutil.copy(file, GHERKIN_TEST_DATA_DIR)


if __name__ == "__main__":
    prepare_data()
