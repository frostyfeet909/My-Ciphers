import os
from os import path
import pathlib
import subprocess
import sys
import importlib


def get_location():
    """Returns the absolute file path"""
    return path.dirname(path.realpath(__file__))


def make_dirs():
    location = path.join(get_location(), "src")

    if not path.isdir(location):
        print("src not found")
        return False

    results = [path.join(location, "resources")]
    for result in results:
        if not path.isdir(result):
            os.mkdir(result)
            print("Made: %s" % result)

    files = [
        path.join(location, "resources", "encoded"),
        path.join(location, "resources", "decoded"),
    ]
    for file in files:
        if not path.isfile(file):
            pathlib.Path(file).touch()
            print("Made: %s" % file)

    return True


def install_modules():
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("requirements.txt not found")
        return False

    installed = True

    for line in lines:
        line = line.strip()
        print("Importing: %s" % line)

        try:
            importlib.import_module(line)
        except ImportError:
            print("Attempting to install: %s" % line)
            try:
                subprocess.call([sys.executable, "-m", "pip", "install", line])
            except:
                print("Could not install: %s" % line)
                installed = False
            else:
                print("Installed: %s" % line)

    return installed


def run():
    if make_dirs() and install_modules():
        print("Completed succesfully")
    else:
        print("Something went wrong")


if "__main__" == __name__:
    run()
