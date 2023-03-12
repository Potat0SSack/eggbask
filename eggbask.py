import os
import pathlib
import configparser
import subprocess
import glob
import sys
import click


@click.group()
def add():
    '''Commands to add and configure emulators/ports'''
    pass


@add.command()
def addemu():
    """Add emulator profile to be used when launching ROMS"""

    name = click.prompt("Type in the emulator name (i.e Project64)")

    a = False
    while a is False:  # we do this to make sure the user won't have to change the profile manually later
        executable = click.prompt(
            "\nType in the full path to executable (i.e C:\\Program Files (x86)\\Project64\\Project64.exe)")
        if os.path.isfile(executable) is False:
            click.secho(
                "Error: Given file or directory not found, please try again.",
                bg="red",
                bold=True)
        else:
            a = True

    b = False
    while b is False:
        config = click.prompt(
            "\nType in the full path to config file (i.e C:\\Program Files (x86)\\Project64\\Config\\Project64.ini). If you don't need it type in None")
        if os.path.isfile(config) or config == "None":
            b = True
        else:
            click.secho(
                "Error: Given file or directory not found, please try again.",
                bg="red",
                bold=True)

    os.makedirs(os.path.dirname("./profiles/"), exist_ok=True)
    filename = name.replace(' ', '-').lower()
    path = "./profiles/" + filename + ".ini"

    profile = configparser.ConfigParser()
    profile.add_section("EmuInfo")
    profile.set("EmuInfo", "name", name)
    profile.set("EmuInfo", "executable", executable)
    profile.set("EmuInfo", "config", config)
    profile.add_section("Extensions")
    profile.set("Extensions", "supported", "None")

    with open(path, "w") as profile_file:
        profile.write(profile_file)

    click.secho("\nEmulator Profile Generated!", bg='green', bold=True)


@add.command()
def addport():
    """Add a game port profile"""

    name = click.prompt("Type in the port name (i.e Ship of Harkinian)")

    a = False
    while a is False:
        executable = click.prompt(
            "\nType in the full path to executable "
            r"(i.e C:\Users\Link\Saved Games\Ship of Harkinian\soh.exe)")
        if os.path.isfile(executable) is False:
            click.secho(
                "Error: Given file or directory not found, please try again.",
                bg="red",
                bold=True)
        else:
            a = True

    b = False
    while b is False:
        config = click.prompt(
            "\nType in the full path to config file (i.e Ship of Harkinian\\shipofharkinian.json). If you don't need it type in None")
        if os.path.isfile(config) or config == "None":
            b = True
        else:
            click.secho(
                "Error: Given file or directory not found, please try again.",
                bg="red",
                bold=True)

    os.makedirs(os.path.dirname("./profiles/ports/"), exist_ok=True)
    filename = name.replace(' ', '-').lower()
    path = "./profiles/ports/" + filename + ".ini"

    profile = configparser.ConfigParser()
    profile.add_section("PortInfo")
    profile.set("PortInfo", "name", name)
    profile.set("PortInfo", "executable", executable)
    profile.set("PortInfo", "config", config)

    with open(path, "w") as profile_file:
        profile.write(profile_file)

    click.secho("\nPort Profile Generated!", bg='green', bold=True)


@add.command()
def addromfolder():
    """Add a ROM folder to pick from when using runrom"""

    a = False
    while a is False:
        folder = click.prompt(
            "Type in the full path to the folder containing your roms (No recursive scanning so the directory needs to have roms, not subfolders with roms)")
        if os.path.isdir(folder) is False:
            click.secho(
                "Error: Given file or directory not found, please try again.",
                bg="red",
                bold=True)
        else:
            a = True

    os.makedirs(os.path.dirname("./profiles/roms/"), exist_ok=True)
    folder_config = os.path.basename(os.path.normpath(folder))
    folder_config = folder_config.replace(' ', '-').lower()
    path = "./profiles/roms/" + folder_config + ".ini"

    profile = configparser.ConfigParser()
    profile.add_section("FolderPath")
    profile.set("FolderPath", "path", folder)

    with open(path, "w") as profile_file:
        profile.write(profile_file)

    click.secho("Rom folder added!", bg='green', bold=True)


@click.group()
def run():
    '''Commands to run emulator/port/rom'''
    pass


@run.command()
def runemu():
    """Run the emulator executable"""

    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\*.ini"))

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Profiles directory has no emulator profiles, make one using 'addemu' command and try again.",
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
        click.echo("Running " + location + "...")
        subprocess.run([location])

    except configparser.NoSectionError:
        click.secho(
            "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'addemu'.",
            bg="red",
            bold=True)


@run.command()
def runport():
    """Run a game port executable"""

    configs_grabbed = []
    configs_grabbed.extend(glob.glob(".\\profiles\\ports\\*.ini"))

    click.echo('\n')
    click.echo('\n'.join(configs_grabbed))

    if len(configs_grabbed) == 0:
        click.secho(
            "Error: Ports directory has no port profiles, make one using 'addport' command and try again.",
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
        click.echo("Running " + location + "...")
        subprocess.run([location])

    except configparser.NoSectionError:
        click.secho(
            "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'addemu'.",
            bg="red",
            bold=True)


@run.command('runrom')
def runrom():
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
                "Error: Profiles directory has no emulator profiles, make one using 'addemu' command and try again.",
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
                        "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'addemu'.",
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
                        "Error: Given .ini file does not contain [EmuInfo] section, your emulator profile may be incorrectly formated, regenerate it via 'addemu'.",
                        bg="red",
                        bold=True)

    except FileNotFoundError:
        click.secho(
            "Error: eggbask did not find a single profile in the 'profiles' directory! Please create one using 'addemu'.",
            bg="red",
            bold=True)


# We do this so that all groups can be called via 'eggbask [command]' and
# by extension for them to appear in --help
cli = click.CommandCollection(sources=[add, run])

if __name__ == '__main__':
    click.secho(r"""
  _____            ____            _
 | ____|__ _  __ _| __ )  __ _ ___| | __
 |  _| / _` |/ _` |  _ \ / _` / __| |/ /
 | |__| (_| | (_| | |_) | (_| \__ \   <
 |_____\__, |\__, |____/ \__,_|___/_|\_\
       |___/ |___/
            """, fg="yellow")
    cli()
