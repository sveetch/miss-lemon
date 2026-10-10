import json

from click.testing import CliRunner
try:
    import rich_click  # noqa: F401
except ImportError:
    IS_RICH_CLICK = False
else:
    IS_RICH_CLICK = True

from miss_lemon.cli.entrypoint import cli_frontend


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


def test_check_rich(caplog, settings):
    """
    Output of report with Rich should be a correct preview tree.

    TODO: Conditionate this test to rich package installation
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure" / "0100_models"

    result = runner.invoke(cli_frontend, ["check", str(source)])

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []

    assert result.output == "\n".join([
        "🎨 Rich tree preview",
        "{}".format(source),
        "├── 0200_lookups <- 002_lookups",
        "├── 0100_managers <- 001_managers",
        "│   └── 0101_blog.py <- 001_blog.py",
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

    result = runner.invoke(cli_frontend, ["check", str(source), "--output", "tree"])

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []

    assert result.output == "\n".join([
        "🎨 Big Tree preview",
        "{}".format(source),
        "├── 0200_lookups <- 002_lookups",
        "├── 0100_managers <- 001_managers",
        "│   └── 0101_blog.py <- 001_blog.py",
        "├── 0001_category.py <- 0103_category.py",
        "└── nada.py (IGNORED)",
        "",
        "",
    ])


def test_check_step(caplog, settings):
    """
    Output of report with Big Tree should be a correct preview tree.
    """
    runner = CliRunner()

    source = settings.datas_path / "minimal_structure" / "0100_models"

    result = runner.invoke(
        cli_frontend,
        ["check", str(source), "--output", "tree", "--step", "10"]
    )

    # from miss_lemon.utils.tests import debug_click_invoke
    # debug_click_invoke(result, caplog)

    assert result.exit_code == 0

    assert caplog.record_tuples == []

    assert result.output == "\n".join([
        "🎨 Big Tree preview",
        "{}".format(source),
        "├── 020_lookups <- 002_lookups",
        "├── 010_managers <- 001_managers",
        "│   └── 011_blog.py <- 001_blog.py",
        "├── 001_category.py <- 0103_category.py",
        "└── nada.py (IGNORED)",
        "",
        "",
    ])
