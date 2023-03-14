import os
import glob
import sys
import configparser
import click

@click.group()
def config():
    '''Commands to configure emulators/ports/romfolders'''
    pass

@config.command('emu')
@click.option('-edit', prompt=True,
               type=click.Choice(['profile', 'config'], case_sensitive=False), help="Select what should be opened")
def emu(edit):

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

    a = False

    while a is False:
        selection = click.prompt(
            "\nPlease type in the appropriate profile .ini (No path required)")
        if os.path.isfile("./profiles/" + selection) is False:
            click.secho(
                "Error: Given .ini not found, make sure you wrote the filename + extension exactly as was displayed above and try again.",
                bg="red",
                bold=True)
        else:
            a = True
    
    if edit == 'profile':
        osCommandString = "notepad.exe " + "./profiles/"  + selection
        os.system(osCommandString)

    elif edit == 'config':
        emu = configparser.ConfigParser()
        emu.read_file(open('./profiles/' + selection))
        config_file = emu.get("EmuInfo", "config")

        if config_file == 'None':
            click.secho(
                "Error: Selected profile does not point to a config file, add one by running this command with -edit=profile and try again.",
                bg='red',
                bold=True)
            sys.exit()
        
        if os.path.isfile(config_file) is False:
            click.secho(
                "Error: Selected profile points to a config file that was either not found, or doesn't exist! Check if the path is correct by running this command with -edit=profile and try again.",
                bg='red',
                bold=True
            )
            sys.exit()
        
        osCommandString = "notepad.exe " + config_file
        os.system(osCommandString)

@config.command('port')
@click.option('-edit', prompt=True,
               type=click.Choice(['profile', 'config'], case_sensitive=False))

def port(edit):

    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\profiles\ports\*.ini"))

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Profiles directory has no port profiles, make one using 'add port' command and try again.",
            bg="red",
            bold=True)
        sys.exit()

    a = False

    while a is False:
        selection = click.prompt(
            "\nPlease type in the appropriate profile .ini (No path required)")
        if os.path.isfile("./profiles/ports/" + selection) is False:
            click.secho(
                "Error: Given .ini not found, make sure you wrote the filename + extension exactly as was displayed above and try again.",
                bg="red",
                bold=True)
        else:
            a = True
    
    if edit == 'profile':
        osCommandString = "notepad.exe " + "./profiles/ports/"  + selection
        os.system(osCommandString)

    elif edit == 'config':
        emu = configparser.ConfigParser()
        emu.read_file(open('./profiles/ports/' + selection))
        config_file = emu.get("PortInfo", "config")

        if config_file == 'None':
            click.secho(
                "Error: Selected profile does not point to a config file, add one by running this command with -edit=profile and try again.",
                bg='red',
                bold=True)
            sys.exit()
        
        if os.path.isfile(config_file) is False:
            click.secho(
                "Error: Selected profile points to a config file that was either not found, or doesn't exist! Check if the path is correct by running this command with -edit=profile and try again.",
                bg='red',
                bold=True
            )
            sys.exit()
        
        osCommandString = "notepad.exe " + config_file
        os.system(osCommandString)
