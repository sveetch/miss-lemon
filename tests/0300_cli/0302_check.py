import json

import pytest

from click.testing import CliRunner
try:
    import rich_click  # noqa: F401
except ImportError:
    IS_RICH_CLICK = False
else:
    IS_RICH_CLICK = True

from miss_lemon.cli.entrypoint import cli_frontend
# from miss_lemon.utils.tests import debug_click_invoke


def test_check_required(caplog):
    """
    At least, the source argument is required.
    """
    runner = CliRunner()

    result = runner.invoke(cli_frontend, ["check"])

    assert result.exit_code == 2

    assert caplog.record_tuples == []

    if IS_RICH_CLICK is True:
        assert "Missing argument 'SOURCE'." in result.output
    else:
        assert "Error: Missing argument 'SOURCE'." in result.output


def test_check_json(caplog, settings):
    """
    Output of report with JSON should be a valid JSON.
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure" / "0100_models"

    result = runner.invoke(cli_frontend, ["check", str(source), "--output", "json"])

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []
    assert json.loads(result.output) == {
        "path": "{}".format(source),
        "number": 0,
        "prefix": "",
        "original_prefix": "",
        "name": "0100_models",
        "children": [
            {
                "path": "{}/001_managers".format(source),
                "number": 100,
                "prefix": "0100",
                "original_prefix": "001",
                "name": "managers",
                "children": [
                    {
                        "path": "{}/001_managers/001_blog.py".format(source),
                        "number": 101,
                        "prefix": "0101",
                        "original_prefix": "001",
                        "name": "blog.py",
                        "children": [],
                        "built_name": "0101_blog.py"
                    }
                ],
                "built_name": "0100_managers"
            },
            {
                "path": "{}/002_lookups".format(source),
                "number": 200,
                "prefix": "0200",
                "original_prefix": "002",
                "name": "lookups",
                "children": [],
                "built_name": "0200_lookups"
            },
            {
                "path": "{}/0103_category.py".format(source),
                "number": 1,
                "prefix": "0001",
                "original_prefix": "0103",
                "name": "category.py",
                "children": [],
                "built_name": "0001_category.py"
            }
        ],
        "built_name": "0100_models"
    }


@pytest.mark.skipif(IS_RICH_CLICK is False, reason="Rich is not installed")
def test_check_rich(caplog, settings):
    """
    Output of report with Rich should be a correct preview tree.

    NOTE: If Rich is installed it becomes the default output, so all other tests will
    probably explitely use the Big tree output 'tree'.
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure" / "0100_models"

    result = runner.invoke(cli_frontend, ["check", str(source), "--exit-1"])
    assert result.exit_code == 1
    assert caplog.record_tuples == []
    assert result.output == "\n".join([
        "🎨 Rich tree preview",
        "{}".format(source),
        "├── 0100_managers/ <- 001_managers/",
        "│   └── 0101_blog.py <- 001_blog.py",
        "├── 0200_lookups/ <- 002_lookups/",
        "└── 0001_category.py <- 0103_category.py",
        "Aborted.",
        "",
    ])

    result = runner.invoke(
        cli_frontend,
        ["check", str(source), "--display-ignored"]
    )
    assert result.exit_code == 0
    assert caplog.record_tuples == []
    assert result.output == "\n".join([
        "🎨 Rich tree preview",
        "{}".format(source),
        "├── 0100_managers/ <- 001_managers/",
        "│   └── 0101_blog.py <- 001_blog.py",
        "├── 0200_lookups/ <- 002_lookups/",
        "├── 0001_category.py <- 0103_category.py",
        "└── nada.py (IGNORED)",
        "",
    ])


def test_check_bigtree(caplog, settings):
    """
    Output of report with Big Tree should be a correct preview tree.
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure" / "0100_models"

    result = runner.invoke(
        cli_frontend,
        ["check", str(source), "--output", "tree", "--exit-1"]
    )
    # debug_click_invoke(result, caplog)
    assert result.exit_code == 1
    assert caplog.record_tuples == []
    assert result.output == "\n".join([
        "🎨 Big Tree preview",
        "{}".format(source),
        "├── 0100_managers/ <- 001_managers/",
        "│   └── 0101_blog.py <- 001_blog.py",
        "├── 0200_lookups/ <- 002_lookups/",
        "└── 0001_category.py <- 0103_category.py",
        "",
        "Aborted.",
        "",
    ])

    result = runner.invoke(
        cli_frontend,
        ["check", str(source), "--output", "tree", "--display-ignored"]
    )
    assert result.exit_code == 0
    assert caplog.record_tuples == []
    assert result.output == "\n".join([
        "🎨 Big Tree preview",
        "{}".format(source),
        "├── 0100_managers/ <- 001_managers/",
        "│   └── 0101_blog.py <- 001_blog.py",
        "├── 0200_lookups/ <- 002_lookups/",
        "├── 0001_category.py <- 0103_category.py",
        "└── nada.py (IGNORED)",
        "",
        "",
    ])


def test_check_step_identical(caplog, settings):
    """
    Step option should change the computation of prefixes. Also with the minimal
    structure, this step value leads to an identical destination for '0100_models'.
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure"

    result = runner.invoke(
        cli_frontend,
        ["check", str(source), "--output", "tree", "--step", "10"]
    )
    assert result.exit_code == 0
    assert caplog.record_tuples == []
    assert result.output == "\n".join([
        "🎨 Big Tree preview",
        "{}".format(source),
        "├── 0100_models/ (SAME)",
        "│   ├── 0110_managers/ <- 001_managers/",
        "│   │   └── 0111_blog.py <- 001_blog.py",
        "│   ├── 0120_lookups/ <- 002_lookups/",
        "│   └── 0101_category.py <- 0103_category.py",
        "├── 0200_views/ <- 1000_views/",
        "└── 0001_foo.py <- 020_foo.py",
        "",
        "",
    ])


def test_check_bigtree_empty(caplog, tmp_path):
    """
    When no resource is eligible to rename, output a message and stop there, exit signal
    code is always 0.
    """
    runner = CliRunner()

    foo = tmp_path / "01_foo.py"
    foo.write_text("# Dummy")
    bar = tmp_path / "bar.py"
    bar.write_text("# Dummy")

    result = runner.invoke(
        cli_frontend,
        ["check", str(tmp_path), "--output", "tree", "--step", "10", "--exit-1"]
    )
    assert result.exit_code == 0
    assert caplog.record_tuples == []
    assert result.output == "Nothing to rename.\n"


@pytest.mark.skipif(IS_RICH_CLICK is False, reason="Rich is not installed")
def test_check_rich_empty(caplog, tmp_path):
    """
    When no resource is eligible to rename, output a message and stop there, exit signal
    code is always 0.
    """
    runner = CliRunner()

    foo = tmp_path / "01_foo.py"
    foo.write_text("# Dummy")
    bar = tmp_path / "bar.py"
    bar.write_text("# Dummy")

    result = runner.invoke(
        cli_frontend,
        ["check", str(tmp_path), "--output", "rich", "--step", "10", "--exit-1"]
    )
    assert result.exit_code == 0
    assert caplog.record_tuples == []
    assert result.output == "Nothing to rename.\n"
