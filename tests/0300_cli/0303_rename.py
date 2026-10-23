
from click.testing import CliRunner
try:
    import rich_click  # noqa: F401
except ImportError:
    IS_RICH_CLICK = False
else:
    IS_RICH_CLICK = True

from miss_lemon.cli.entrypoint import cli_frontend


def test_rename_required(caplog):
    """
    At least, the source argument is required.
    """
    runner = CliRunner()

    result = runner.invoke(cli_frontend, ["rename"])

    assert result.exit_code == 2

    assert caplog.record_tuples == []

    if IS_RICH_CLICK is True:
        assert "Missing argument 'SOURCE'." in result.output
    else:
        assert "Error: Missing argument 'SOURCE'." in result.output


def test_rename_basic(caplog, basic_structure):
    """
    On default, the command will output a shell script with 'mv' command lines to
    apply renaming.
    """
    runner = CliRunner()

    result = runner.invoke(cli_frontend, ["rename", str(basic_structure)])

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []

    assert result.output == "\n".join([
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.",
        "cd '{}';".format(basic_structure),
        (
            "mv '0100_models/001_managers/001_blog.py' "
            "'0100_models/001_managers/01101_blog.py';"
        ),
        (
            "mv '0100_models/001_managers/002_article.py' "
            "'0100_models/001_managers/01102_article.py';"
        ),
        "mv '0100_models/0101_blog.py' '0100_models/01001_blog.py';",
        "mv '0100_models/0102_article.py' '0100_models/01002_article.py';",
        "mv '0100_models/0103_category.py' '0100_models/01003_category.py';",
        "mv '0100_models/010_base.py' '0100_models/01004_base.py';",
        "mv '010_base/010_ok.txt' '010_base/02001_ok.txt';",
        "mv '010_base/030_cool.bak.py' '010_base/02002_cool.bak.py';",
        "mv '0500_forms/502_article.py' '0500_forms/04001_article.py';",
        "mv '020_foo.py' '00001_foo.py';",
        "mv '1020_bar.py' '00002_bar.py';",
        "mv '0100_models/001_managers' '0100_models/01100_managers';",
        "mv '0100_models/002_lookups' '0100_models/01200_lookups';",
        "mv '0100_models' '01000_models';",
        "mv '010_base' '02000_base';",
        "mv '0200_empty' '03000_empty';",
        "mv '0500_forms' '04000_forms';",
        "mv '1000_views' '05000_views';",
        "echo \"Finished all tasks!\";",
        "",
        "",
    ])


def test_rename_step(caplog, minimal_structure):
    """
    With step option.
    """
    runner = CliRunner()

    result = runner.invoke(
        cli_frontend,
        ["rename", str(minimal_structure), "--step", "10"]
    )

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []

    assert result.output == "\n".join([
        "# This shell script will 'cd' into the source directory then apply renaming "
        "of resources.",
        "cd '{}';".format(minimal_structure),
        (
            "mv '0100_models/001_managers/001_blog.py' "
            "'0100_models/001_managers/0111_blog.py';"
        ),
        "mv '0100_models/0103_category.py' '0100_models/0101_category.py';",
        "mv '020_foo.py' '0001_foo.py';",
        "mv '0100_models/001_managers' '0100_models/0110_managers';",
        "mv '0100_models/002_lookups' '0100_models/0120_lookups';",
        "mv '1000_views' '0200_views';",
        "echo \"Finished all tasks!\";",
        "",
        "",
    ])


def test_rename_no_available_resource(caplog, tmp_path):
    """
    When renamer do not find any eligible (non ignored, non identical) resource, it
    will raise an error and exit with error signal.
    """
    runner = CliRunner()

    foo = tmp_path / "01_foo.py"
    foo.write_text("# Dummy")
    bar = tmp_path / "bar.py"
    bar.write_text("# Dummy")

    result = runner.invoke(
        cli_frontend,
        ["rename", str(tmp_path), "--step", "10"]
    )

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)
    assert result.output == "There was no resource eligible to renaming.\nAborted.\n"

    assert result.exit_code == 1

    assert caplog.record_tuples == []
