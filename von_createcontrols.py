# ------------------------------------------------------------------------
#    Import Required Controls -- NEEDS CLEANUP
# ------------------------------------------------------------------------

import bpy, json, pprint, bmesh, os, sys, mathutils # type: ignore
from bpy import context # type: ignore
from bpy.types import Operator # type: ignore 
from bpy_extras.object_utils import object_data_add # type: ignore
from mathutils import Vector # type: ignore
from math import radians
import pathlib
from . import von_buttoncontrols
from .von_buttoncontrols import *

# ------------------------------------------------------------------------
#    Create General Functions
# ------------------------------------------------------------------------

def spaceconsole(temp):
    xx = temp
    while xx > 0:
        xx = xx -1
        print("")
#for pose mode
def setcontrol(temp_controlname):
    bpy.ops.object.mode_set(mode = 'POSE')
    controlname=str(temp_controlname)
    bpy.context.active_pose_bone.custom_shape = bpy.data.objects[controlname]


# ------------------------------------------------------------------------
#    Create Saving Functions
# ------------------------------------------------------------------------
def create_json_data_from_mesh():
    mesh_object = bpy.context.active_object
    data = get_mesh_data(mesh_object)
    save_data(data)


def save_data(data):
    path_to_file = getfolderloc()+"//"+"controls//"+data["object_name"]+".json"
    print(path_to_file)
    with open(path_to_file, "w") as out_file_obj:
        text = json.dumps(data, indent=4)
        out_file_obj.write(text)

def saveselectedmesh():
    bpy.ops.object.editmode_toggle()
    create_json_data_from_mesh()

# ------------------------------------------------------------------------
#    Create Loading Functions
# ------------------------------------------------------------------------


def load_data(nameoffile):
    path_to_file = getfolderloc()+"//"+"controls"+"//"+nameoffile+".json"
    with open(path_to_file, "r") as in_file_obj:
        text = in_file_obj.read()
        data = json.loads(text)

    return data


def get_mesh_data(mesh_object):
    bmesh_obj = bmesh.from_edit_mesh(mesh_object.data)
    face_to_vert = []
    for face in bmesh_obj.faces:
        face_verts = []
        for vert in face.verts:
            face_verts.append(vert.index)
        face_to_vert.append(face_verts)
    vert_count = len(bmesh_obj.verts)
    vert_coords = [None] * vert_count
    for vert in bmesh_obj.verts:
        vert_coords[vert.index] = list(vert.co)
    bpy.ops.object.editmode_toggle()
    data = {
        "object_name": mesh_object.name,
        "face_verts": face_to_vert,
        "vert_coordinates": vert_coords,
    }
    return data

def create_mesh_from_json_data(shouldskeletonise,nameoffile):

    mesh_data = load_data(nameoffile)
    create_mesh_from_data(mesh_data,shouldskeletonise)

def setname(data,shouldskeletonise):
    object_name = data["object_name"]
    object_name = "CNTRL_"+object_name
    if shouldskeletonise == True:
        object_name = object_name + "_Skeletonised"
    if shouldskeletonise == False:
        object_name = object_name + "_Solid"
    return object_name

def create_mesh_from_data(data,shouldskeletonise):
    bpy.ops.object.mode_set(mode = 'OBJECT')
    faces = data["face_verts"]
    verts = data["vert_coordinates"]
    edges = []

    object_found = False
    object_name = data["object_name"]
    object_name = "CNTRL_"+object_name
    if shouldskeletonise == True:
        object_name = object_name + "_Skeletonised"
    if shouldskeletonise == False:
        object_name = object_name + "_Solid"
    for o in bpy.context.scene.objects:
        if o.name == object_name:
            object_found = True
            break
    
            

    if object_found == True:
         print("objectname is in listallobjects")
    elif object_found == False:
        mesh_data = bpy.data.meshes.new(f"{object_name}_data")
        mesh_data.from_pydata(verts, edges, faces)
        mesh_obj = bpy.data.objects.new(object_name, mesh_data)
        bpy.context.collection.objects.link(mesh_obj)
        if shouldskeletonise == True:
            bpy.context.view_layer.objects.active = mesh_obj
            bpy.ops.object.mode_set(mode = 'EDIT')
                
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.delete(type='ONLY_FACE')

            bpy.context.view_layer.objects.active = mesh_obj
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.context.view_layer.objects.active = mesh_obj
        movetocollection("Controls",object_name)


def movetocollection(NameOfCollection,object_name):
    list_collection = []


    collectionFound = False


    for myCol in bpy.data.collections:
        if myCol.name == NameOfCollection:
            collectionFound = True
            break
            
            
    if collectionFound == False:
        myCol = bpy.data.collections.new(NameOfCollection)
        bpy.context.scene.collection.children.link(myCol)
        

 #-----------
    
    obj = bpy.context.scene.objects.get(object_name)
    if obj:
        bpy.context.view_layer  .active_layer_collection.collection.objects.unlink(obj)
        myCol.objects.link(obj)

    bpy.data.collections[NameOfCollection].hide_viewport = True
        




# ------------------------------------------------------------------------
#    Create Multiuse Functions
# ------------------------------------------------------------------------

def getobjectdata(controldata):
    file = open(controldata+'.txt')
    
def getfolderloc():
    dir = os.path.dirname(os.path.abspath(__file__))
    if not dir in sys.path:
        sys.path.append(dir)
    return(dir)

def get_path_to_folderloc():
    spaceconsole(10)
    meshdatafile = str(getfolderloc())
    print()
    spaceconsole(10)
    return meshdatafile

def organisetocontrolscollection(createdobjectname):
    collectiontomoveto = "Controls Collection"
    collectionexists = False


    #Check if the controls collection already exists and add it in (In a way that is visible to the user in the default viewport outliner) if it doesn't
    for collections in bpy.data.collections:
        if collections.name == collectiontomoveto:
            collectionexists = True
            break
    
    if collectionexists == True:
        print("Collection Exists")
    object = bpy.context.active_object
    if collectionexists == False:
        #Create And Link Custom Collection
        collection = bpy.data.collections.new(collectiontomoveto)
        bpy.context.scene.collection.children.link(collection)
    

    collectiontomoveto = bpy.data.collections[collectiontomoveto]

    bpy.context.collection.objects.unlink(object)
    
    collectiontomoveto.objects.link(object)

# ------------------------------------------------------------------------
#    Create Weight Hammer Functions
# ------------------------------------------------------------------------

def getnearbyvertexinfo(selectedvertex):
    #relies on KDTree Utilities - https://docs.blender.org/api/current/mathutils.kdtree.html
    obj = context.object

    mesh = obj.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)




# ------------------------------------------------------------------------
#    Test Controls
# ------------------------------------------------------------------------