from pydoc import ispath
from venv import create
import bpy # type: ignore
from .Libraries.pythonlibraries.pillow.PIL import Image # type: ignore
from .von_common import *
import os, bmesh # type: ignore

#---------------------------------------------------------------------------------------------------------------#

                                                #Gather Data

#---------------------------------------------------------------------------------------------------------------#

def get_mesh_materials(targetMesh):
    print("Running ---- get_mesh_materials ---- Running")
    materialsDict = {}
    for materialIndex in targetMesh.material_slots:
        material = materialIndex.material
        if material:
            materialsDict[targetMesh] = material
    print("FINISHED")
    return materialsDict

def get_meshes_materials(targetMeshes):
    print("Running ---- get_meshes_materials ---- Running")
    materialsDict = {}
    for targetmesh in targetMeshes:
        materialsList = []
        for materialIndex in targetmesh.material_slots:
            material = materialIndex.material
            if material:
                materialsList = materialsList + material
        materialsDict[targetmesh] = materialsList

    print("FINISHED")
    return materialsDict

#materialName needs the **STRING** name input, not the object - If there are errors print out materialName and materialSlot before bug checking anything else
def get_image_paths_from_material(obj, materialName, self):
    print("Running ---- get_image_paths_from_material ---- Running")
    materialDict = {}
    typesOfSocket = []
    materialDict[materialName] = {}
    material = False

    for materialSlot in obj.material_slots:
        if materialSlot.material.name == materialName:
            material = materialSlot.material
            break
    if not material:
            reporterror(self, f"{materialName} not found or doesn't use nodes.")
    
    principledNode = None
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principledNode = node
            break

    if not principledNode:
        reporterror(self, f"No Principled BSDF node found in {materialName}.")
        return materialDict, typesOfSocket

    for inputSocket in principledNode.inputs:
        if inputSocket.is_linked:
            socketName = inputSocket.name
            materialDict[materialName][socketName] = []
            if inputSocket.name  not in typesOfSocket:
                typesOfSocket = typesOfSocket + [inputSocket.name]

            for link in inputSocket.links:
                fromNode = link.from_node
                if fromNode.type == 'TEX_IMAGE':
                    image = fromNode.image
                    if image and image.filepath:
                        absPath = bpy.path.abspath(image.filepath)
                        if absPath not in materialDict[materialName][socketName]:
                            materialDict[materialName][socketName].append(absPath)
    print("FINISHED")
    return materialDict, typesOfSocket
"""
matdict looks like:
Object
  -> Material Name
            -> Socket Name
                  -> Link To Texture
"""

def get_all_images_of_socket_type(materialsDict, targetSocket):
    print("Running ---- get_all_images_of_socket_type ---- Running")
    targetLower = targetSocket.lower().replace(" ", "")
    if targetLower == "basecolour": # I am english, I will forget at some point
        targetLower = "basecolor"
    textures = []

    for obj, materialsList in materialsDict.items():
        for materialEntry in materialsList:
            for _, socketDict in materialEntry.items():
                for socketName, imageList in socketDict.items():
                    socketLower = socketName.lower().replace(" ", "")
                    if targetLower == socketLower:
                        textures.extend(imageList)
    print("FINISHED")
    return textures

#---------------------------------------------------------------------------------------------------------------#

                                                #Pack Image

#---------------------------------------------------------------------------------------------------------------#

#JUST BASECOLOUR FOR NOW, EXPAND IN A LOOP ONCE FUNCTIONAL
def pack_materials_into_atlases(self, materialDict, socketTypes, atlasSize=4096):
    """
    Packs multiple maps (BaseColour, Normal, Roughness, etc) for each material
    into the SAME atlas coordinates.
    """
    print("Running ---- pack materials into atlases ---- Running")

    atlasData = {}
    materialsToPack = []

    # Gather material sets
    for matName, matInfo in materialDict.items():
        images = {}
        maxW, maxH = 0, 0

        for socketType in socketTypes:
            imgPath = matInfo.get(socketType)
            isPathTrue = Path(imgPath).is_file()
            print(f"IsPathTrue = {isPathTrue}")
            if imgPath and isPathTrue:
                img = Image.open(imgPath)
                images[socketType] = img
                maxW = max(maxW, img.width)
                maxH = max(maxH, img.height)

        if images:
            materialsToPack.append((matName, images, maxW, maxH))

    # Sort biggest first (optional)
    materialsToPack.sort(key=lambda x: x[3], reverse=True)
    print("Checkpoint 1")
    atlasImages = {stype: Image.new("RGBA", (atlasSize, atlasSize), (0, 0, 0, 0))
                   for stype in socketTypes}
    atlasIndex = 1
    cursorX, cursorY, rowHeight = 0, 0, 0

    for matName, images, blockW, blockH in materialsToPack:
        # Check if fits current row
        if cursorX + blockW > atlasSize:
            cursorX = 0
            cursorY += rowHeight
            rowHeight = 0

        # Check if fits in atlas vertically
        if cursorY + blockH > atlasSize:
            # Save current atlases, start new ones
            for stype in socketTypes:
                yield f"Atlas_{atlasIndex}_{stype}", atlasImages[stype]
            atlasIndex += 1
            atlasImages = {stype: Image.new("RGBA", (atlasSize, atlasSize), (0, 0, 0, 0))
                           for stype in socketTypes}
            cursorX, cursorY, rowHeight = 0, 0, 0

        # Paste each map at SAME coords
        for stype in socketTypes:
            img = images.get(stype)
            if img:
                atlasImages[stype].paste(img, (cursorX, cursorY))

        # Record coords once (shared by all sockets)
        for stype in socketTypes:
            atlasData.setdefault(matName, {})[stype] = {
                "atlasName": f"Atlas_{atlasIndex}_{stype}",
                "x": cursorX, "y": cursorY,
                "width": blockW, "height": blockH
            }

        cursorX += blockW
        rowHeight = max(rowHeight, blockH)

    # Save last batch
    for stype in socketTypes:
        yield f"Atlas_{atlasIndex}_{stype}", atlasImages[stype]
    spaceconsole(5)
    print("ATLAS DATA IN PACK MATERIALS?????")
    print(atlasData)
    spaceconsole(5)
    return atlasData






 #Undo System ->

def store_original(obj, settings):
    print("Running ---- store_original ---- Running")
    entry = settings.original_data.add()
    entry.object_name = obj.name
    entry.mesh_name = obj.data.name
    for slot in obj.material_slots:
        mat_entry = entry.materials.add()
        mat_entry.name = slot.material.name if slot.material else ""

def restore_original(obj, settings):
    print("Running ---- restore_original ---- Running")
    entry = next((e for e in settings.original_data if e.object_name == obj.name), None)
    if not entry:
        print(f"No stored data for {obj.name}")
        return None
    mesh = bpy.data.meshes.get(entry.mesh_name)
    if mesh:
        obj.data = mesh
    for i, mat_entry in enumerate(entry.materials):
        mat = bpy.data.materials.get(mat_entry.name)
        if mat and i < len(obj.material_slots):
            obj.material_slots[i].material = mat

def duplicate_for_atlas(obj):
    print("Running ---- duplicate_for_atlas ---- Running")
    obj.data = obj.data.copy()
    for i, slot in enumerate(obj.material_slots):
        if slot.material:
            new_mat = slot.material.copy()
            new_mat.name = f"{slot.material.name}_atlas"
            obj.material_slots[i].material = new_mat

def save_atlas_images(atlasImages, outputDir):
    print("Running --- save atlas images --- RUNNING")
    Path(outputDir).mkdir(parents=True, exist_ok=True)
    for name, img in atlasImages.items():
        filePath = Path(outputDir) / f"{name}.png"
        img.save(filePath)
    print("FINISHED")
#---------------------------------------------------------------------------------------------------------------#

                                                #Move UV's

#---------------------------------------------------------------------------------------------------------------#

def update_material_uvs(obj, atlasData, atlasSize=4096):
    """
    Shifts & scales UVs of an object so that they match
    the atlas coordinates from atlasData.
    Assumes each material shares one rect across all maps.
    """
    print("Running ---- Update_material_UV's ---- Running")
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)

    uv_layer = bm.loops.layers.uv.verify()

    for face in bm.faces:
        # Get material name
        matIndex = face.material_index
        if matIndex >= len(obj.material_slots):
            continue
        matName = obj.material_slots[matIndex].name

        # Grab any one socket’s data (all sockets share the same coords now)
        matAtlasInfo = None
        if matName in atlasData:
            # just take the first socket entry
            matAtlasInfo = next(iter(atlasData[matName].values()))

        if not matAtlasInfo:
            continue

        # Compute offset + scale
        uOffset = matAtlasInfo["x"] / atlasSize
        vOffset = matAtlasInfo["y"] / atlasSize
        uScale = matAtlasInfo["width"] / atlasSize
        vScale = matAtlasInfo["height"] / atlasSize

        # Apply to each loop (face corner)
        for loop in face.loops:
            uv = loop[uv_layer].uv
            uv.x = uOffset + uv.x * uScale
            uv.y = vOffset + uv.y * vScale

    bm.to_mesh(me)
    bm.free()
    print("FINISHED")
