#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Import For menu
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import bpy # type: ignore
from .operators import *


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Menu
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class VonPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonTools'
    bl_options = {"DEFAULT_CLOSED"}

class VONPANEL_PT_primary_panel(VonPanel, bpy.types.Panel):
    bl_idname = "VONPANEL_PT_primary_panel"
    bl_label= "Von Tools"

    def draw(self,context):
        scene = context.scene
        common_data = scene.common_data
        layout = self.layout
        layout.label(text= "Texture Atlasing Toolset!")
        box = layout.box()
        row = box.row()
        row.prop(common_data, "atlas_size")
        row.prop(common_data, "atlas_output_path")
        row = box.row()
        row.prop(common_data, "atlas_moveUVs")
        if common_data.atlas_moveUVs:
            row = box.row()
            row.prop(common_data, "atlas_applymaterial")
            if common_data.atlas_applymaterial:
                row.prop(common_data, "atlas_output_path")
        layout = self.layout
        layout.operator("von.optimisationtools_textureatlasing", text="Texture Atlas")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# For Registering
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
classes = [
    VONPANEL_PT_primary_panel
]


def register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)    

def nregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)