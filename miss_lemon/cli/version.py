try:
    import rich_click as click
except ImportError:
    import click

from miss_lemon import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("miss-lemon {}".format(__version__))
