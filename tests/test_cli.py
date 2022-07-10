from reformat_gherkin.cli import main

from .helpers import GHERKIN_TEST_DATA_DIR, options_to_cli_args


def test_cli_success(runner, sources):
    result = runner.invoke(main, sources(contain_invalid=False))

    assert len(result.stdout) == 0
    assert result.exit_code == 0
    assert result.stderr.startswith("Reformatted")


def test_cli_stdin_success(runner, valid_contents):
    for content, expected, options in valid_contents(
        with_expected=True,
        with_options=True,
    ):
        args = options_to_cli_args(options) + ["-"]
        args.remove("--check")
        args = " ".join(args)
        result = runner.invoke(main, args=args, input=content)

        assert result.stdout == expected
        assert result.exit_code == 0
        assert result.stderr.startswith("Reformatted stdin")


def test_cli_check(runner, sources):
    result = runner.invoke(
        main,
        [
            *sources(contain_invalid=False),
            "--check",
        ],
    )

    assert len(result.stdout) == 0
    assert result.exit_code == 1
    assert result.stderr.startswith("Would reformat")


def test_cli_check_gherkin_test_data(runner):
    result = runner.invoke(
        main,
        [
            str(GHERKIN_TEST_DATA_DIR.absolute()),
            "--check",
        ],
    )
    assert len(result.stdout) == 0
    assert result.exit_code == 1
    assert result.stderr.startswith("Would reformat")


def test_cli_stdin_check(runner, valid_contents):
    for content in valid_contents():
        args = " ".join(["-", "--check"])
        result = runner.invoke(main, args=args, input=content)

        assert len(result.stdout) == 0
        assert result.exit_code == 1


def test_cli_failed(runner, sources):
    result = runner.invoke(
        main,
        [
            *sources(),
            "--check",
        ],
    )

    assert len(result.stdout) == 0
    assert result.exit_code == 123


def test_cli_empty_sources(runner):
    result = runner.invoke(main)

    assert len(result.stdout) == 0
    assert result.exit_code == 0


def test_cli_check_with_valid_config(runner, sources):
    result = runner.invoke(
        main,
        sources(
            contain_invalid=False,
            with_config_file=True,
        ),
    )

    assert len(result.stdout) == 0
    assert result.exit_code == 1
    assert result.stderr.startswith("Using configuration from")


def test_cli_check_with_invalid_config(runner, sources):
    result = runner.invoke(
        main,
        sources(
            contain_invalid=False,
            with_config_file=True,
            valid_config=False,
        ),
    )

    assert len(result.stdout) == 0
    assert result.exit_code == 1
    assert result.stderr.startswith("Error: Could not open file")


def test_cli_check_with_empty_config(runner, sources):
    result = runner.invoke(
        main,
        sources(
            contain_invalid=False,
            with_config_file=True,
            empty_config=True,
        ),
    )

    assert len(result.stdout) == 0
    assert result.exit_code == 0
