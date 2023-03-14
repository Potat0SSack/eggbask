import click

from commands.add import add as add
from commands.run import run as run

@click.group()
def entry_point():
    pass

entry_point.add_command(add)
entry_point.add_command(run)


if __name__ == '__main__':
    click.secho(r"""
  _____            ____            _
 | ____|__ _  __ _| __ )  __ _ ___| | __
 |  _| / _` |/ _` |  _ \ / _` / __| |/ /
 | |__| (_| | (_| | |_) | (_| \__ \   <
 |_____\__, |\__, |____/ \__,_|___/_|\_\
       |___/ |___/
            """, fg="yellow"
        )
    
    entry_point()
