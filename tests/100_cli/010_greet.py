import pytest

from click.testing import CliRunner

from miss_lemon.cli.entrypoint import cli_frontend


APPLABEL = "miss-lemon"


@pytest.mark.skip("Deprecated")
def test_greet_basic(caplog):
    """
    The command is executable without any arguments and then should greet the
    world in plain text.
    """
    runner = CliRunner()

    # Invoke the commandline from the CliRunner
    result = runner.invoke(cli_frontend, ["greet"])

    # To debug logs on fail
    # Commandline full output
    print("=> result.output <=")
    print(result.output)
    print()
    # Recorded logs as tuples
    print("=> caplog.record_tuples <=")
    print(caplog.record_tuples)
    print()
    # Raise possible exception from commandline, useful when there is an
    # unexpected exception during execution
    print("=> result.exception <=")
    print(result.exception)
    if result.exception:
        raise result.exception

    # Success signal from execution
    assert result.exit_code == 0

    # Expected basic output
    assert result.output == "Hello world!\n"

    # Empty logs is expected
    assert caplog.record_tuples == []


@pytest.mark.skip("Deprecated")
def test_greet_custom_name(caplog):
    """
    The command is executable without any arguments and then should greet the
    world in plain text.
    """
    runner = CliRunner()

    # Invoke the commandline from the CliRunner
    result = runner.invoke(cli_frontend, ["greet", "foobar"])

    # Success signal from execution
    assert result.exit_code == 0

    # Expected basic output
    assert result.output == "Hello foobar!\n"

    # Empty logs is expected
    assert caplog.record_tuples == []
