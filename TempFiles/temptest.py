ENUM_STRING_CACHE = {}
def intern_enum_items_strings(items):
    def intern_string(s):
        if isinstance(s, str):
            ENUM_STRING_CACHE.setdefault(s, s)
            s = ENUM_STRING_CACHE[s]
        return s

    return [
        tuple([intern_string(s) for s in item])
        for item in items
    ]




bpy.types.Mesh.my_shapekey = bpy.props.EnumProperty( # type: ignore
    name="My Shapekey",
    description="Select a shapekey",
    items=my_shapekey_enum_items_callback, # type: ignore
)



class CamShapeMaticPanel(bpy.types.Panel): # type: ignore
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CamShpMtc'
    bl_label = "CamShapeMatic"
    bl_idname = "camshapematic.panel"

    def draw(self, context):
        layout = self.layout

        # draw my_shapekey for the current object
        # only if it's a mesh with shapekeys though
        if (
            context and
            context.object and
            context.object.type == 'MESH' and
            context.object.data.shape_keys
        ):
            layout.prop(context.object.data, "my_shapekey")


bpy.utils.register_class(CamShapeMaticPanel) # type: ignore