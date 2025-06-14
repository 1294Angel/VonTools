import bpy # type: ignore
import os
import sys

from .von_menu_popup import von_menupopup_register, von_menupopup_unregister


bl_info = {
    "name": "Vona's Blender Tools",
    "author": "Vona",
    "version": (0, 3, 2),
    "blender": (4, 2, 10),
    "location": "Where the user can find it",
    "description": "Gold Version of Vona's addon that adds tools to expand blenders toolset.",
    "warning": "",
    "wcooliki_url": "",
    "tracker_url": "",
    "category": ""}


print("VonTools Reloaded!")
print("Python version:", sys.version)
print("Working dir:", os.getcwd())


def register():
    von_menupopup_register()
def unregister():
    von_menupopup_unregister()

if __name__ == "__main__":
    von_menupopup_register()