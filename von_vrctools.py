import bpy # type: ignore #ignore
from pathlib import Path
from . import von_createcontrols

def gatherheirarchydata():
    directory_path = von_createcontrols.getfolderloc()
    for file in directory_path.iterdir():
        if file.is_file():  # Check if it is a file
            print(f"File: {file.name}")  # Process the file (e.g., print its name)
    