import os
import configparser
import click

@click.group()
def add():
    '''Commands to add emulators/ports/romfolders'''
    pass


@add.command()
def emu():
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
def port():
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
def romfolder():
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