import click


@click.group()
def cli():
    pass


@cli.command()
def hello():
    click.echo('Hello, World!')

@cli.command
@click.argument('day', type=int)
@click.argument('part', type=int)
def run(day, part):
    click.echo(f'Running day {day} part {part}...')