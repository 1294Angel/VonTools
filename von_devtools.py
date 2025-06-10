import bpy # type: ignore

def spaceconsole(temp):
    xx = temp
    while xx > 0:
        xx = xx -1
        print("")

def reporterror(self, e):
    self.report({'ERROR'}, f"Unexpected Error: {str(e)}")

def getselectedarmatures(context):
    return [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
    """I've been using this version, but checking selected objects seems more efficient
    [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]"""

def get_meshes_using_armature(armature_obj):
    controlled_meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature_obj:
                    controlled_meshes.append(obj)
                    break
    return controlled_meshes

def get_armature_for_mesh(mesh_obj):
    for mod in mesh_obj.modifiers:
        if mod.type == 'ARMATURE' and mod.object:
            return mod.object
    return None