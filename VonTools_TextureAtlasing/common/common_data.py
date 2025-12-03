import bpy # type: ignore




# ----------------------
# Basic Property Group
# ----------------------
class common_data(bpy.types.PropertyGroup):
    atlas_size: bpy.props.IntProperty(
        name="Atlas Size",
        description="Size of each atlas sheet generated, system will generate multiple if all existing textures don't fit in the given atlas resolution",
        default = 4096
        ) # type: ignore
    atlas_output_path: bpy.props.StringProperty(
        name = "Atlas Export Filepath",
        description = "Where will the generated atlas/'s be stored on your device?",
        default = "",
        subtype = "FILE_PATH"
    ) # type: ignore
    atlas_simplepack = bpy.props.BoolProperty(
        name="Simple Packing?",
        description="Packs the materials in a simple, rapid way. Turn off for complex packing. (NOT WORKING ATM)",
        default=True,
        subtype='TOGGLE'   # 'NONE', 'LAYER', 'TOGGLE', 'FILE_PATH', 'DIR_PATH'
    )
    atlas_moveUVs: bpy.props.BoolProperty(
        name="Move UV's?",
        description="Move the object's UV's to match the new locations of the newly created atlas trimsheet.",
        default=True,
    ) # type: ignore
    atlas_applymaterial: bpy.props.BoolProperty(
        name="Apply Material?",
        description="Remove all old materials and replace them with the new trimsheet material.",
        default=True,
    ) # type: ignore
    atlas_materialname: bpy.props.StringProperty(
        name = "Atlas Material Name",
        description = "What will the atlas material be called?",
        default = "atlas_material",
        maxlen = 100
    ) # type: ignore

# ----------------------
# Registration
# ----------------------
classes = [
    common_data
]

def register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.common_data = bpy.props.PointerProperty(type=common_data)

def unregister():
    del bpy.types.Scene.common_data
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)