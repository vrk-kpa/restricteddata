import click
import sys
from ckan.plugins import toolkit
from . import categories
from .migrate import Migrate, plan_to_path
from .migrations import migrations


def get_commands():
    return [restricteddata, content]


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


@click.group()
def content():
    'Content modification tools'
    pass


@content.command()
@click.pass_context
@click.argument('current_version')
@click.argument('target_version')
@click.option(u'--dryrun', is_flag=True)
@click.option(u'--path-index', type=int)
def migrate(ctx, current_version, target_version, dryrun, path_index):
    'Migrates site content from one version to another'
    m = Migrate()

    for v1, v2, step in migrations():
        m.add(v1, v2, step)

    plans = m.plan(current_version, target_version)

    if not plans:
        click.secho(f'No migration paths found from {current_version} to {target_version}')
        sys.exit(1)
    elif len(plans) > 1:
        if path_index is None:
            click.secho(f'Multiple migration paths found from {current_version} to {target_version}.')
            click.secho('Run this command again with the option --path-index <your selection>')
            for i, plan in enumerate(plans):
                click.secho('{}: {}'.format(i, ' -> '.join(plan_to_path(plan))))
            sys.exit(1)

        plan = plans[int(path_index)]
    else:
        plan = plans[0]

    click.secho('Using migration path: {}'.format(' -> '.join(plan_to_path(plan))))

    if dryrun:
        click.secho('Performing a dry run')

    for v1, v2, step in plan:
        click.secho('Migrating from {} to {}'.format(v1, v2))
        step(ctx, toolkit.config, dryrun, echo=click.secho)

    click.secho('Finished migration successfully')
