import click
from . import categories


def get_commands():
    return [restricteddata]


@click.group()
def restricteddata(short_help=u"Restricted data commands."):
    """Restricted data commands.
    """
    pass


@ restricteddata.command()
@ click.pass_context
@ click.option('-d', '--dryrun', is_flag=True)
def create_default_categories(context, dryrun: bool) -> None:
    click.secho("create_default_categories - BEGIN")
    categories.create(context, dryrun)


@ restricteddata.command()
@ click.pass_context
@ click.option('-d', '--dryrun', is_flag=True)
@ click.option('-p', '--purge', is_flag=True)
def delete_default_categories(context, dryrun: bool, purge: bool) -> None:
    click.secho("delete_default_categories - BEGIN")
    categories.delete(context, dryrun, purge)

