import bpy # type: ignore

def reporterror(self, message:str):
    self.report({'ERROR'}, f"Unexpected Error: {str(message)}")

def getselectedarmatures(context):
    return [obj for obj in context.selected_objects if obj.type == 'ARMATURE']

def get_meshes_from_armature(armature_obj):
    controlled_meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature_obj:
                    controlled_meshes.append(obj)
                    break
    return controlled_meshes

def get_armature_for_mesh(mesh_obj):
    armaturelist = []
    for mod in mesh_obj.modifiers:
        if mod.type == 'ARMATURE' and mod.object:
            armaturelist.append(mod.object)
    if armaturelist:
        return armaturelist
    return None

def get_selected_meshes(context):
    selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
    return selected_meshes