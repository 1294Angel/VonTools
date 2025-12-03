import bpy # type: ignore
from . import operators
from . import menu
from .common import common_data

bl_info = {
    "name": "Vona's Texture Atlas Toolset",
    "author": "Vona",
    "version": (0, 0, 1),
    "blender": (5, 0, 0),
    "location": "Where the user can find it",
    "description": "Gold Version of Vona's addon that adds tools to expand blenders toolset.",
    "warning": "",
    "wcooliki_url": "",
    "tracker_url": "",
    "category": ""}


def register():
    common_data.register()
    operators.register()
    menu.register()
    

def unregister():
    menu.unregister()
    operators.unregister()
    common_data.unregister()