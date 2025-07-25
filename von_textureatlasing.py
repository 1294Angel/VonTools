import bpy # type: ignore
from .Libraries.pythonlibraries.pillow.PIL import Image # type: ignore
from .von_common import *

#---------------------------------------------------------------------------------------------------------------#

                                                #Gather Data

#---------------------------------------------------------------------------------------------------------------#

def get_mesh_materials(targetMesh):
    materialsDict = {}
    for materialIndex in targetMesh.material_slots:
        material = materialIndex.material
        if material:
            materialsDict[targetMesh] = material
    return materialsDict

def get_meshes_materials(targetMeshes):
    materialsDict = {}
    for targetmesh in targetMeshes:
        materialsList = []
        for materialIndex in targetmesh.material_slots:
            material = materialIndex.material
            if material:
                materialsList = materialsList + material
        materialsDict[targetmesh] = materialsList
    return materialsDict

#materialName needs the **STRING** name input, not the object - If there are errors print out materialName and materialSlot before bug checking anything else
def get_image_paths_from_material(obj, materialName, self):
    materialDict = {}
    materialDict[materialName] = {}
    material = False

    for materialSlot in obj.material_slots:
        if materialSlot.material.name == materialName:
            material = materialSlot.material
            break
    if not material:
            reporterror(self, f"Material not found or doesn't use nodes.")
            return material
    
    principledNode = None
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principledNode = node
            break

    if not principledNode:
        reporterror(self, f"No Principled BSDF node found in material.")
        return materialDict

    for inputSocket in principledNode.inputs:
        if inputSocket.is_linked:
            socketName = inputSocket.name
            materialDict[materialName][socketName] = []

            for link in inputSocket.links:
                fromNode = link.from_node
                if fromNode.type == 'TEX_IMAGE':
                    image = fromNode.image
                    if image and image.filepath:
                        absPath = bpy.path.abspath(image.filepath)
                        if absPath not in materialDict[materialName][socketName]:
                            materialDict[materialName][socketName].append(absPath)

    return materialDict
            


#---------------------------------------------------------------------------------------------------------------#

                                                #Pack Image

#---------------------------------------------------------------------------------------------------------------#




#---------------------------------------------------------------------------------------------------------------#

                                                #Move UV's

#---------------------------------------------------------------------------------------------------------------#
