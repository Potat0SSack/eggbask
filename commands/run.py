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

    try:
        emu = configparser.ConfigParser()
        emu.read_file(open("./profiles/" + selection))
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

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Ports directory has no port profiles, make one using 'add port' command and try again.",
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

    try:
        emu = configparser.ConfigParser()
        emu.read_file(open("./profiles/ports/" + selection))
        location = emu.get("PortInfo", "executable")
        click.secho("Running " + location + "...", bg='blue', bold=True)
        subprocess.run([location])

    except configparser.NoSectionError:
        click.secho(
            "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'addemu'.",
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
            click.echo('\n'.join(folders_grabbed))

            x = False
            while x is False:
                rom_folder = click.prompt(
                    "Please type in the desired folder .ini")
                if os.path.isfile("./profiles/roms/" + rom_folder) is False:
                    click.secho(
                        "Error: Given .ini is not found.",
                        bg="red",
                        bold=True)
                else:
                    x = True

            folder = configparser.ConfigParser()
            folder.read_file(open("./profiles/roms/" + rom_folder))
            rom_location = folder.get("FolderPath", "path")

            roms_grabbed = []
            roms_grabbed.extend(os.path.basename(x)
                                for x in glob.glob(rom_location + "/*"))

            click.echo('\n')
            click.echo('\n'.join(roms_grabbed))

        a = False
        while a is False:
            rom = click.prompt(
                "\n Please type in the path to desired ROM including extension")
            if os.path.isfile(rom_location + "/" + rom) is False:
                click.secho(
                    "Error: Given ROM is not found.",
                    bg="red",
                    bold=True)
            else:
                userom = rom_location + "/" + rom
                a = True

            path = pathlib.Path('./profiles')
            file_extension = pathlib.Path(rom).suffix
            click.echo(file_extension)

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
                            file_extension +
                            " found! Launching " +
                            rom +
                            " using " +
                            cur_path +
                            "...",
                            bg="blue")

                        emu = configparser.ConfigParser()
                        emu.read_file(open(cur_path))
                        location = emu.get("EmuInfo", "executable")

                        subprocess.call([location, userom])
                        sys.exit()
                    else:
                        click.echo(
                            file_extension + " not found in " + cur_path)
                        continue

            elif os.path.isdir(cur_path):
                # Making an assumption that the only subdiretories here is the
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
        click.echo('\n'.join(configs_grabbed))

        b = False

        while b is False:
            selection = click.prompt(
                "\nPlease type in the appropriate profile .ini (No path required)")
            if os.path.isfile("./profiles/" + selection) is False:
                click.secho(
                    "Error: Given .ini not found, make sure you wrote the filename + extension exactly as was displayed above and try again.",
                    bg="red",
                    bold=True)
            b = True

            confirm = click.confirm(
                "Do you want to assign " +
                file_extension +
                " to " +
                selection +
                " emulator?")

            if confirm:

                try:
                    emu = configparser.ConfigParser()
                    emu.read_file(open("./profiles/" + selection))
                    extension_file = open("./profiles/" + selection, 'r')
                    data = extension_file.read()
                    extension_number = data.count('extension') + 1
                    emu.set("Extensions", "supported" + str(extension_number), file_extension)

                    click.echo("Adding extension to config...")
                    with open("./profiles/" + selection, "w") as profile_file:
                        emu.write(profile_file)
                        click.secho("Extension added!", bg="green")

                    location = emu.get("EmuInfo", "executable")
                    click.secho(
                        "Running " +
                        rom +
                        " with " +
                        location +
                        "...",
                        bg="blue")
                    subprocess.call([location, userom])
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
                        rom +
                        " with " +
                        location +
                        "...",
                        bg="blue")
                    subprocess.call([location, userom])
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
    """Run a ROM file using an added emulator"""

    click.echo('\n')

    try:

        use_folder = click.confirm("Browse added folders?")
        if use_folder:
            folders_grabbed = []
            folders_grabbed.extend(glob.glob("./profiles/roms/*.ini"))

            click.echo('\n')
            click.echo('\n'.join(folders_grabbed))

            x = False
            while x is False:
                rom_folder = click.prompt(
                    "Please type in the desired folder .ini")
                if os.path.isfile("./profiles/roms/" + rom_folder) is False:
                    click.secho(
                        "Error: Given .ini is not found.",
                        bg="red",
                        bold=True)
                else:
                    x = True

            folder = configparser.ConfigParser()
            folder.read_file(open("./profiles/roms/" + rom_folder))
            rom_location = folder.get("FolderPath", "path")

            roms_grabbed = []
            roms_grabbed.extend(os.path.basename(x)
                                for x in glob.glob(rom_location + "/*"))

            click.echo('\n')
            click.echo('\n'.join(roms_grabbed))

        a = False
        while a is False:
            rom = click.prompt(
                "\n Please type in the path to desired ROM including extension")
            if os.path.isfile(rom_location + "/" + rom) is False:
                click.secho(
                    "Error: Given ROM is not found.",
                    bg="red",
                    bold=True)
            else:
                userom = rom_location + "/" + rom
                a = True

            path = pathlib.Path('./profiles')
            file_extension = pathlib.Path(rom).suffix
            click.echo(file_extension)

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
                            file_extension +
                            " found! Launching " +
                            rom +
                            " using " +
                            cur_path +
                            "...",
                            bg="blue")

                        emu = configparser.ConfigParser()
                        emu.read_file(open(cur_path))
                        location = emu.get("EmuInfo", "executable")

                        subprocess.call([location, userom])
                        sys.exit()
                    else:
                        click.echo(
                            file_extension + " not found in " + cur_path)
                        continue

            elif os.path.isdir(cur_path):
                # Making an assumption that the only subdiretories here is the
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
        click.echo('\n'.join(configs_grabbed))

        b = False

        while b is False:
            selection = click.prompt(
                "\nPlease type in the appropriate profile .ini (No path required)")
            if os.path.isfile("./profiles/" + selection) is False:
                click.secho(
                    "Error: Given .ini not found, make sure you wrote the filename + extension exactly as was displayed above and try again.",
                    bg="red",
                    bold=True)
            b = True

            confirm = click.confirm(
                "Do you want to assign " +
                file_extension +
                " to " +
                selection +
                " emulator?")

            if confirm:

                try:
                    emu = configparser.ConfigParser()
                    emu.read_file(open("./profiles/" + selection))
                    emu.set("Extensions", "supported", file_extension)

                    click.echo("Adding extension to config...")
                    with open("./profiles/" + selection, "w") as profile_file:
                        emu.write(profile_file)
                        click.secho("Extension added!", bg="green")

                    location = emu.get("EmuInfo", "executable")
                    click.secho(
                        "Running " +
                        rom +
                        " with " +
                        location +
                        "...",
                        bg="blue")
                    subprocess.call([location, userom])
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
                        rom +
                        " with " +
                        location +
                        "...",
                        bg="blue")
                    subprocess.call([location, userom])
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
