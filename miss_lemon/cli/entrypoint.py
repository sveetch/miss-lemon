"""
Main entrance to commandline actions
"""
try:
    import rich_click as click
except ImportError:
    import click
else:
    # This is rich-click option only to show arguments in help
    click.rich_click.SHOW_ARGUMENTS = True

from miss_lemon.logger import init_logger

from miss_lemon import __pkgname__
from miss_lemon.cli.version import version_command
from miss_lemon.cli.check import check_command
from miss_lemon.cli.rename import rename_command


# Help alias on "-h" argument
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


# Default logger conf
APP_LOGGER_CONF = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", None)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-v", "--verbose",
    type=click.IntRange(min=0, max=5),
    default=4,
    metavar="INTEGER",
    help=(
        "An integer between 0 and 5, where '0' make a totaly "
        "silent output and '5' set level to DEBUG (the most verbose "
        "level). Default to '4' (Info level)."
    )
)
@click.pass_context
def cli_frontend(ctx, verbose):
    """
    Script for application commandline entrypoint.
    """
    printout = True
    if verbose == 0:
        verbose = 1
        printout = False

    # Verbosity is the inverse of logging levels
    levels = [item for item in APP_LOGGER_CONF]
    levels.reverse()
    # Init the logger config
    root_logger = init_logger(
        __pkgname__,
        levels[verbose],
        printout=printout
    )

    # Init the default context that will be passed to commands
    ctx.obj = {
        "verbosity": verbose,
        "logger": root_logger,
    }


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(check_command, name="check")
cli_frontend.add_command(rename_command, name="rename")
