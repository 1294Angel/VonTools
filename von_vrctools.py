import bpy, os # type: ignore
from pathlib import Path
from . import von_createcontrols


def get_addon_directory():
    # Get the directory of the current Python file
    addon_directory = os.path.dirname(__file__)
    return addon_directory

def gatherheirarchydata():
    directory_path = get_addon_directory()
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)  # Create the full file path
        if os.path.isfile(file_path):  # Check if it is a file
            print(f"File: {filename}")  # Process the file (e.g., print its name)sdawsd