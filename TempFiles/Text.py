import bpy # type: ignore

def updatebonestandarizationoptions_enum():
    return {
        "Option 1": ["Choice A", "Choice B", "Choice C"],
        "Option 2": ["Choice D", "Choice E"],
        "Option 3": ["Choice F", "Choice G", "Choice H", "Choice I"],
        "Option 4": ["Choice J", "Choice K"],
        "Option 5": ["Choice J", "Choice K"],
        "Option 6": ["Choice J", "Choice K"],  # Add more options as needed
    }

class MySettings(bpy.types.PropertyGroup):
    pass

def register_dynamic_properties():
    options = updatebonestandarizationoptions_enum()
    for option in options:
        prop_name = option.lower().replace(' ', '_') + "_choice"
        choices = [(choice, choice, "") for choice in options[option]]
        setattr(MySettings, prop_name, bpy.props.EnumProperty(
            name=option.replace('_', ' ').title(),
            items=choices
        ))


class ShowBonePanel(bpy.types.Panel):
    """Creates a Panel for the Bone Standardization menu."""
    bl_label = "Bone Standardization Menu"
    bl_idname = "OBJECT_PT_show_bone_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bone Options'  # New tab name for the panel
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        # Access the properties and draw dropdowns
        props = context.scene.my_tool
        options = updatebonestandarizationoptions_enum()
        itterations = 0
        for option in options.keys():
            itterations = itterations + 1
            print(f"GENERATING {itterations}")
            prop_name = option.lower().replace(' ', '_') + "_choice"
            layout.prop(props, prop_name)


classes = (
ShowBonePanel,
MySettings
)

def register():
    print(f'Menu File Initiated')
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_class(ShowBonePanel)
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(MySettings)

if __name__ == "__main__":
    register()
