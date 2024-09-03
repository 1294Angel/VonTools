import bpy # type: ignore
import os
import sys

from . import (
    von_createcontrols,
    von_menu_popup,
    von_buttoncontrols
)
from .von_menu_popup import (von_menupopup_register, von_menupopup_unregister)

ADDON_FOLDER_PATH = os.path.dirname(__file__)

bl_info = {
    "name": "Vona's Blender Tools",
    "author": "Vona",
    "version": (0, 1, 1),
    "blender": (4, 2, 1),
    "location": "Where the user can find it",
    "description": "Gold Version of Vona's addon that adds tools to expand blenders toolset.",
    "warning": "",
    "wcooliki_url": "",
    "tracker_url": "",
    "category": ""}



def register():
    print(f'Init Folder initiated')
    von_menupopup_register()
    sys.path.append(ADDON_FOLDER_PATH)
def unregister():
    von_menupopup_unregister()

if __name__ == "__main__":
    von_menupopup_register()