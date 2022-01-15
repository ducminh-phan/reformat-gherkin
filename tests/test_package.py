import os


def test_run_as_package_success(sources):
    args = " ".join(sources(contain_invalid=False))
    exit_code = os.system(f"python -m reformat_gherkin {args}")

    assert exit_code == 0


def test_run_as_package_check(sources):
    args = " ".join(sources(contain_invalid=False))
    exit_code = os.system(f"python -m reformat_gherkin --check {args}")

    assert exit_code == 1


def test_run_as_package_failed(sources):
    args = " ".join(sources())
    exit_code = os.system(f"python -m reformat_gherkin --check {args}")

    assert exit_code == 1
