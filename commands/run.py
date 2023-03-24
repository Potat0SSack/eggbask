import os
import configparser
import sys
import glob
import subprocess
import click
import pathlib


@click.group()
def run():
    '''Commands to run emulator/port/rom'''
    pass


@run.command()
def emu():
    """Run the emulator executable"""

    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\*.ini"))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Profiles directory has no emulator profiles, make one using 'add emu' command and try again.",
            bg="red",
            bold=True)
        sys.exit()

    click.echo('\n')
    for count, value in enumerate(configs_grabbed, start=1):
        click.echo('{} - {}'.format(count, value))

    while True:
        try:
            choice = click.prompt("\nSelect your desired emulator (number or name + .ini)")
            
            if choice.isdigit():
                choice = int(choice)
                selection = configs_grabbed[choice - 1]
                
            else:
                if os.path.isfile("./profiles/" + choice) is False:
                    click.echo("Invalid filename, please try again.")
                    continue
                
                selection = "./profiles/" + choice
                
        except IndexError:
            click.echo("Invalid value, please try again.")
            continue
        else:
            break


    try:
        emu = configparser.ConfigParser()
        emu.read_file(open(selection))
        location = emu.get("EmuInfo", "executable")
        click.secho("Running " + location + "...", bg='blue', bold=True)
        subprocess.run([location])

    except configparser.NoSectionError:
        click.secho(
            "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'add emu'.",
            bg="red",
            bold=True)


@run.command()
def port():
    """Run a game port executable"""

    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\ports\\*.ini"))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Ports directory has no port profiles, make one using 'add port' command and try again.",
            bg="red",
            bold=True)
        sys.exit()

    click.echo('\n')
    for count, value in enumerate(configs_grabbed, start=1):
        click.echo('{} - {}'.format(count, value))

    
    while True:
        try:
            choice = click.prompt("\nSelect your desired port (number or name + .ini)")
            
            if choice.isdigit():
                choice = int(choice)
                selection = configs_grabbed[choice - 1]
                
            else:
                if os.path.isfile("./profiles/ports/" + choice) is False:
                    click.echo("Invalid filename, please try again.")
                    continue
                
                selection = "./profiles/ports/" + choice
                
        except IndexError:
            click.echo("Invalid value, please try again.")
            continue
        else:
            break

    try:
        emu = configparser.ConfigParser()
        emu.read_file(open(selection))
        location = emu.get("PortInfo", "executable")
        click.secho("Running " + location + "...", bg='blue', bold=True)
        subprocess.run([location])

    except configparser.NoSectionError:
        click.secho(
            "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formatted, regenerate it via 'add emu'.",
            bg="red",
            bold=True)


@run.command('rom')
def rom():
    """Run a ROM file using an added emulator"""

    click.echo('\n')

    try:

        use_folder = click.confirm("Browse added folders?")
        if use_folder:
            folders_grabbed = []
            folders_grabbed.extend(glob.glob("./profiles/roms/*.ini"))
            
            click.echo('\n')
            for count, value in enumerate(folders_grabbed, start=1):
                click.echo('{} - {}'.format(count, value))

            while True:
                try:
                    choice = click.prompt("\nSelect your desired folder (number or name + .ini)")
                    
                    if choice.isdigit():
                        choice = int(choice)
                        folder = configparser.ConfigParser()
                        folder.read_file(open(folders_grabbed[choice - 1]))
                        rom_location = folder.get("FolderPath", "path")
                        
                    else:
                        folder = configparser.ConfigParser()
                        if os.path.isfile("./profiles/roms/" + choice) is False:
                            click.echo("Invalid filename, please try again.")
                            continue
                            
                        folder.read_file(open("./profiles/roms/" + choice))
                        rom_location = folder.get("FolderPath", "path")
                        
                except IndexError:
                    click.echo("Invalid value, please try again.")
                    continue
                else:
                    break

            roms_grabbed = []
            roms_grabbed.extend(os.path.basename(x)
                                for x in glob.glob(rom_location + "/*"))

            for count, value in enumerate(roms_grabbed, start=1):
                click.echo('{} - {}'.format(count, value))
        
        while True:
                try:
                    choice = click.prompt("\nSelect your desired rom (full path + name + .extension)")

                    if os.path.isfile(choice) is False:
                        click.echo("Invalid filename, please try again.")
                        continue
                        
                    path = pathlib.Path('./profiles')
                    file_extension = pathlib.Path(choice).suffix
                    click.echo(file_extension)
                        
                except IndexError:
                    click.echo("Invalid value, please try again.")
                    continue
                else:
                    break
            
            
        # We one by one go through each config and look for any mention of the
        # given rom extension
        for file in os.listdir(path):

            cur_path = os.path.join(path, file)
            click.echo(cur_path)

            if os.path.isfile(cur_path):

                with open(cur_path, 'r') as file:
                    click.echo(file)

                    if file_extension in file.read():
                        click.secho(
                            "File extension found in " + cur_path, bg="green")
                        click.secho(
                            "Valid emulator config for " +
                            str(file_extension) +
                            " found! Launching " +
                            str(choice) +
                            " using " +
                            cur_path +
                            "...",
                            bg="blue")

                        emu = configparser.ConfigParser()
                        emu.read_file(open(cur_path))
                        location = emu.get("EmuInfo", "executable")

                        subprocess.call([location, choice])
                        sys.exit()
                    else:
                        click.echo(
                            file_extension + " not found in " + cur_path)
                        continue

            elif os.path.isdir(cur_path):
                # Making an assumption that the only subdirectories here is the
                # "ports" and "roms" thus, no need to check them
                click.echo("Encountered a directory, ignoring.")
                continue

        click.secho("\nNo valid config has been found!", bg='yellow')
        configs_grabbed = []
        configs_grabbed.extend(glob.glob(".\\profiles\\*.ini"))

        if len(configs_grabbed) == 0:
            click.secho(
                "Error: Profiles directory has no emulator profiles, make one using 'add emu' command and try again.",
                bg="red",
                bold=True)
            sys.exit()

        click.echo('\n')
        for count, value in enumerate(configs_grabbed, start=1):
            click.echo('{} - {}'.format(count, value))

        while True:
            try:
                choice = click.prompt("\nSelect your desired emulator (number or name + .ini)")
                
                if choice.isdigit():
                    choice = int(choice)
                    selection = configs_grabbed[choice - 1]
                    
                else:
                    if os.path.isfile("./profiles/" + choice) is False:
                        click.echo("Invalid filename, please try again.")
                        continue
                    
                    selection = "./profiles/" + choice
                    
            except IndexError:
                click.echo("Invalid value, please try again.")
                continue
            else:
                break

        confirm = click.confirm(
            "Do you want to assign " +
            file_extension +
            " to " +
            selection +
            " emulator?")

        if confirm:

            try:
                emu = configparser.ConfigParser()
                emu.read_file(open(selection))
                extension_file = open(selection, 'r')
                data = extension_file.read()
                extension_number = data.count('extension') + 1
                emu.set("Extensions", "supported" + str(extension_number), file_extension)

                click.echo("Adding extension to config...")
                with open(selection, "w") as profile_file:
                    emu.write(profile_file)
                    click.secho("Extension added!", bg="green")

                location = emu.get("EmuInfo", "executable")
                click.secho(
                    "Running " +
                    str(choice) +
                    " with " +
                    location +
                    "...",
                    bg="blue")
                subprocess.call([location, choice])
                sys.exit()

            except configparser.NoSectionError:
                click.secho(
                    "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'add emu'.",
                    bg="red",
                    bold=True)

            # If only i could have a function that can dynamically
            # change according to the case instead of ctrl+c ctrl+v
            # with minor tweaks for given section...
        else:                
            try:
                emu = configparser.ConfigParser()
                location = emu.get("EmuInfo", "executable")
                click.secho(
                    "Running " +
                    choice +
                    " with " +
                    location +
                    "...",
                    bg="blue")
                subprocess.call([location, choice])
                sys.exit()

            except configparser.NoSectionError:
                click.secho(
                    "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'add emu'.",
                    bg="red",
                    bold=True)

    except FileNotFoundError:
        click.secho(
            "Error: eggbask did not find a single profile in the 'profiles' directory! Please create one using 'add emu'.",
            bg="red",
            bold=True)
