import bpy # type: ignore
 
from bpy.types import Panel, Operator, PropertyGroup # type: ignore
from bpy.props import EnumProperty, PointerProperty, StringProperty # type: ignore
 
 
class MyProperties(PropertyGroup):
    
    my_enum : EnumProperty(
        name= "Enumerator / Dropdown",
        description= "sample text",
        items= [('OP1', "Append", ""),
                ('OP2', "Remove", "")
        ]
    ) # type: ignore
    new_item : StringProperty() # type: ignore
    my_list = []
 
 
class ADDONNAME_PT_main_panel(Panel):
    bl_label = "Main Panel"
    bl_idname = "ADDONNAME_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "New Tab"
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        
        layout.prop(mytool, "my_enum", expand = True)
        layout.prop(mytool, "new_item")
        layout.operator("addonname.myop_operator")
 
 
class ADDONNAME_OT_my_op(Operator):
    bl_label = "Submit"
    bl_idname = "addonname.myop_operator"
    
    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        list = mytool.my_list
        enum = mytool.my_enum
        new_item = mytool.new_item
        
        print(enum)
    
 
 
 
classes = [MyProperties, ADDONNAME_PT_main_panel, ADDONNAME_OT_my_op]
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.my_tool = PointerProperty(type= MyProperties)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool
 
if __name__ == "__main__":
    register()