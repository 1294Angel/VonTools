import bpy # type: ignore
from .common.common_functions import get_selected_meshes
from .image_packing import *


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Image Packing
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-- Unique Data Storage
class texture_atlas_material_item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()  # type: ignore
    doWork: bpy.props.BoolProperty(name="Include", default=True)  # type: ignore

class texture_atlas_mesh_item(bpy.types.PropertyGroup):
    meshName: bpy.props.StringProperty()  # type: ignore
    materials: bpy.props.CollectionProperty(type=texture_atlas_material_item)  # type: ignore
    
#-- Operators
class von_panel_rig_checker_texture_atlas(bpy.types.Operator):
    bl_idname = "von.optimisationtools_textureatlasing"
    bl_label = "Texture Atlas"

    meshes: bpy.props.CollectionProperty(type=texture_atlas_mesh_item)  # type: ignore

    def invoke(self, context, event):
        self.meshes.clear()
        selectedMeshes = get_selected_meshes(context)
        seenMaterials = set()
        for obj in selectedMeshes:
            meshItem = self.meshes.add()
            meshItem.meshName = obj.name
            for matSlot in obj.material_slots:
                if matSlot.material and matSlot.material.name not in seenMaterials:
                    seenMaterials.add(matSlot.material.name)
                    matItem = meshItem.materials.add()
                    matItem.name = matSlot.material.name

        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        seenMaterials = set()
        box = layout.box()
        box.label(text=("Select Materials To Atlas"))
        for meshItem in self.meshes:
            for matItem in meshItem.materials:
                if matItem.name not in seenMaterials:
                    seenMaterials.add(matItem.name)
                    row = box.row()
                    row.prop(matItem, "doWork", text="")
                    row.label(text=matItem.name)





    def execute(self, context):
        matObjDict = {}        
        matLinkDict = {}
        texturesBySocket = {}
        settings = context.scene.common_data
        atlasSize = settings.atlas_size
        atlasOutputPath = settings.atlas_output_path
        shouldMoveUVs = settings.atlas_moveUVs



        for meshItem in self.meshes:
            obj = bpy.data.objects.get(meshItem.meshName)
            for matItem in meshItem.materials:
                if matItem.doWork == True:
                    matObjDict.setdefault(matItem.name, []).append(obj.name)
            
        matLinkDict = get_all_image_textures_from_discovered_materials(matObjDict)
        texturesBySocket = organise_textures_by_socket(matLinkDict)
        savedPaths, positions = pack_images(self, atlasOutputPath, texturesBySocket, atlasSize)
        if shouldMoveUVs:
            uvMapDict = convert_positions_to_uvs(positions, atlasSize)
            apply_uv_map_to_material_objects(matObjDict, uvMapDict)
        #Expand to include 
        return {'FINISHED'}
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Hardsurface Edge Wear
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# For Registering
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

classes = [
    #Unique data to file
    texture_atlas_material_item,
    texture_atlas_mesh_item,
    #Other Classes
    von_panel_rig_checker_texture_atlas
]


def register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)    

def unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)