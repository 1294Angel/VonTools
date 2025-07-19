import bpy # type: ignore
import os
import sys

from . import von_common
from . import von_menu_popup


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

addon_dir = os.path.dirname(__file__)
pillow_path = os.path.join(addon_dir, "/pillow/", "pillow_lib")
if pillow_path not in sys.path:
    sys.path.append(pillow_path)

def register():
    von_common.von_common_register()
    von_menu_popup.von_menupopup_register()

def unregister():
    von_menu_popup.von_menupopup_unregister()
    von_common.von_common_unregister()