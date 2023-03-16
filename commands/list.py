import glob
import sys
import click

@click.group()
def list():
    '''Commands to list desired profiles'''
    pass

@list.command()
def emu():
    """List all emulator profiles"""
    
    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\*.ini"))

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Profiles directory has no emulator profiles, make one using 'add emu' command and try again.",
            bg="red",
            bold=True)
        sys.exit()
        
@list.command()
def port():
    """List all port profiles"""
    
    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\ports\\*.ini"))

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Ports directory has no port profiles, make one using 'add port' command and try again.",
            bg="red",
            bold=True)
        sys.exit()
        
@list.command()
def romfolder():
    """List all romfolder profiles"""
    
    folders_grabbed = []
    folders_grabbed.extend(glob.glob("./profiles/roms/*.ini"))

    click.echo('\n')
    click.echo('\n'.join(folders_grabbed))
    
    if len(folders_grabbed) == 0:
        click.secho(
            "Error: Roms directory has no rom folder profiles, make one using 'add romfolder' command",
            bg="red",
            bold=True)
        sys.exit()
