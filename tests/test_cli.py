from reformat_gherkin.cli import main


def test_cli_success(runner, sources):
    result = runner.invoke(main, [*sources(contain_invalid=False)])

    assert result.exit_code == 0


def test_cli_check(runner, sources):
    result = runner.invoke(main, [*sources(contain_invalid=False), "--check"])

    assert result.exit_code == 1


def test_cli_failed(runner, sources):
    result = runner.invoke(main, [*sources(), "--check"])

    assert result.exit_code == 123


def test_cli_empty_sources(runner):
    result = runner.invoke(main)

    assert result.exit_code == 0


def test_cli_check_with_valid_config(runner, sources):
    result = runner.invoke(
        main, [*sources(contain_invalid=False, with_config_file=True)]
    )

    assert result.exit_code == 1
    assert result.stdout.startswith("Using configuration from")


def test_cli_check_with_invalid_config(runner, sources):
    result = runner.invoke(
        main,
        [*sources(contain_invalid=False, with_config_file=True, valid_config=False)],
    )

    assert result.exit_code == 1
    assert result.stdout.startswith("Error: Could not open file")


def test_cli_check_with_empty_config(runner, sources):
    result = runner.invoke(
        main,
        [*sources(contain_invalid=False, with_config_file=True, empty_config=True)],
    )

    assert result.exit_code == 0
