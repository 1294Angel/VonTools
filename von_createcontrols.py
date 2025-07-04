# ------------------------------------------------------------------------
#    Import Required Controls -- NEEDS CLEANUP
# ------------------------------------------------------------------------

import bpy, json, pprint, bmesh, os, sys, mathutils # type: ignore
from pathlib import Path # type: ignore
from bpy.types import Operator # type: ignore 
from bpy_extras.object_utils import object_data_add # type: ignore
from mathutils import Vector # type: ignore
from math import radians
from collections import defaultdict
from . import von_buttoncontrols

# ------------------------------------------------------------------------
#    Create General Functions
# ------------------------------------------------------------------------


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
    base_dir = Path(__file__).parent  
    path_to_file = base_dir / "controls" / f"{data['object_name']}.json"
    with open(path_to_file, "w") as out_file_obj:
        json.dump(data, out_file_obj, indent=4)

def saveselectedmesh():
    bpy.ops.object.editmode_toggle()
    create_json_data_from_mesh()

# ------------------------------------------------------------------------
#    Create Loading Functions
# ------------------------------------------------------------------------


def load_data(nameoffile):
    base_dir = Path(__file__).parent  
    path_to_file = base_dir / "controls" / f"{nameoffile}.json"

    with open(path_to_file, "r") as in_file_obj:
        data = json.load(in_file_obj)  # json.load directly from file

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
#    Create Multiuse Functions #Functional
# ------------------------------------------------------------------------

def getobjectdata(controldata):
    file = open(controldata+'.txt')
    
def getfolderloc():
    dir = Path(__file__).resolve().parent
    if str(dir) not in sys.path:
        sys.path.append(str(dir))
    return dir

def get_path_to_folderloc():
    meshdatafile = str(getfolderloc())
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
# ------------------------------
#Gets Connected Vertecies
def getnearbyvertecies_dict():
    mesh = bpy.context.view_layer.objects.active.data  # object must be a mesh and in EditMode

    vertexconnections = {}

    vertexconnections.clear()
    
    selected_verts = [v for v in mesh.vertices if v.select]
    
    bm = bmesh.from_edit_mesh(mesh)
    
    for vert in bm.verts:
        vl = []
        
        for i in selected_verts:
            if i.index == vert.index:
                for l in vert.link_edges:
                    tmpvl = (l.other_vert(vert))
                    vl.append(tmpvl.index)
                vertexconnections[vert.index] = vl
    return vertexconnections

#Returns Dictionary Of Vert Weights and Groups Searchable By Vert
def getallvertices_vertexgroups():
    mesh = bpy.context.view_layer.objects.active.data
    ob = bpy.context.object
    assert ob is not None and ob.type == 'MESH', "active object invalid"
    ob.update_from_editmode()
    
    #Get Selected Verts And Object Data
    selected_verts = [v for v in mesh.vertices if v.select]
    me = ob.data
    # create vertex group lookup dictionary for names
    vgroup_names = {vgroup.index: vgroup.name for vgroup in ob.vertex_groups}

    #get actionable vertecies
    feedverts = getnearbyvertecies_dict()
    
    # create dictionary of vertex group assignments per vertex
    vgroups = {}
    for v in me.vertices:
        addtodict = ()
        for sel in selected_verts:
            for x in feedverts[sel.index]:

                if v.index == x:
                    for g in v.groups:
                        tmpaddtodict = []
                        groupname = vgroup_names[g.group]
                        vertexweight = g.weight
                        tmpaddtodict = tuple([(groupname, vertexweight)])
                        addtodict = addtodict + tmpaddtodict
                    vgroups.update({v.index: addtodict})
    print("Returning vgroups")
    #returns a dictionary in this format --> {vertex index : ((vertexgroup name, vertex weight),(vertexgroup name, vertex weight),ect  )}
    return vgroups


#RUN THIS ONE, ALL THE REST ARE INSIDE IT!!
def averagevertexweights():
    weightdict = getallvertices_vertexgroups()
    vertexgroups = []
    weights = []
    
    for i in weightdict:
        #1,2,4
        dictionary = weightdict[i]
        for item in dictionary:
            vertgroupname = item[0]
            #Each Vertexgroupname

            if vertgroupname in vertexgroups:
                print("fuck no")
                
            elif vertgroupname not in vertexgroups:
                vertexgroups.append(vertgroupname)
    #returns a list of vertex groups on the vertecies -- HAS NO DOUBLES
    #Use this to then search through the verticies of selected items to average out each vertexgroup
    
    for group in vertexgroups:
        weightslist = []
        for i in weightdict:
            dictionary = weightdict[i]
            for item in dictionary:
                if item[0] == group:
                    print("FOUND GROUP")
                    print(group)
                    tmpweighttoadd = item[1]
                    print(item[1])
                    weightslist.append(tmpweighttoadd)
        averagedvertexweight = 0
        iterations = 0
        for it in weightslist:
            iterations = iterations + 1
            averagedvertexweight = averagedvertexweight + it
        averagedvertexweight = averagedvertexweight / iterations
        print(f"Group Assigning = {group} Averaged Vertex Weight - {averagedvertexweight}")
        assignvertexweights(group,averagedvertexweight)

def clear_vertex_weights():
    obj = bpy.context.active_object
    if obj.mode != 'EDIT':
        bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data
    cleared_count = 0
    for v_index in range(len(mesh.vertices)):
        if mesh.vertices[v_index].select:
            for vgroup in obj.vertex_groups:
                obj.vertex_groups[vgroup.index].remove([v_index])
                cleared_count += 1
    bpy.ops.object.mode_set(mode='EDIT')

#Assigns Weights (And checks the vertex groups actually exist)
def assignvertexweights(vertex_group_name, vertex_weight):
    obj = bpy.context.active_object
    mesh = obj.data

    

    if obj and obj.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create or get the vertex group
        if vertex_group_name not in obj.vertex_groups:
            vertex_group = obj.vertex_groups.new(name=vertex_group_name)
        else:
            vertex_group = obj.vertex_groups[vertex_group_name]
        # Assign the selected vertices to the vertex group
        for vert in mesh.vertices:
            if vert.select:  # Check if the vertex is selected
                vertex_group.add([vert.index], vertex_weight, 'REPLACE')

        bpy.ops.object.mode_set(mode='EDIT')
# ------------------------------------------------------------------------
#    Test Controls
# -----------------------------------------------------------------------