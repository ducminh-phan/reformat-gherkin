import subprocess

COMMON_ARGS = "poetry run python -m reformat_gherkin".split()


def test_run_as_package_success(sources):
    args = [
        *COMMON_ARGS,
        *sources(contain_invalid=False),
    ]
    result = subprocess.run(args)

    assert result.returncode == 0


def test_run_as_package_check(sources):
    args = [
        *COMMON_ARGS,
        "--check",
        *sources(contain_invalid=False),
    ]
    result = subprocess.run(args)

    assert result.returncode == 1


def test_run_as_package_failed(sources):
    args = [
        *COMMON_ARGS,
        *sources(),
    ]
    result = subprocess.run(args)

    assert result.returncode == 123
