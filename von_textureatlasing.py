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

        


#---------------------------------------------------------------------------------------------------------------#

                                                #Pack Image

#---------------------------------------------------------------------------------------------------------------#




#---------------------------------------------------------------------------------------------------------------#

                                                #Move UV's

#---------------------------------------------------------------------------------------------------------------#
