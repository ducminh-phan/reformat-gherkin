from reformat_gherkin.core import reformat_stream_or_path
from tests.conftest import TEST_DIR
from tests.helpers import FILENAME_OPTION_MAP


def generate_test_data():
    for feature_dir in (TEST_DIR / "data" / "valid").iterdir():
        if not feature_dir.is_dir():
            continue

        for expected in feature_dir.glob("expected_*.feature"):
            options = FILENAME_OPTION_MAP[expected.stem]
            reformat_stream_or_path(
                feature_dir / "input.feature",
                expected,
                options=options,
            )


if __name__ == "__main__":
    generate_test_data()
