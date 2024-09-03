import bpy # type: ignore
import bmesh # type: ignore

def clearscreen(x):
    for i in range(x):
        print("")

def get_selected_vertex_data(shouldindex):
    clearscreen(1)
    print("getvertexdata running")

    selected_verts_indecies = []
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    selected_verts = [vert for vert in bm.verts if vert.select]
    if shouldindex == True:
        for vert in selected_verts:
            selected_verts_indecies.append(vert.index)
        print("Selected Vert Indecies = " + str(selected_verts_indecies))
        clearscreen(1)
        return(selected_verts_indecies)
    return(selected_verts)

 
def getEdgesForVertex(v_index, mesh, marked_edges):
    all_edges = [e for e in mesh.edges if v_index in e.vertices]
    unmarked_edges = [e for e in all_edges if e.index not in marked_edges]
    return unmarked_edges

def findConnectedVerts(v_index, mesh, connected_verts, marked_edges, maxdepth=1, level=0):
    clearscreen(2)
    print("findConnectedVerts running")
    if level >= maxdepth:
        return
    
    edges = getEdgesForVertex(v_index, mesh, marked_edges)
    print("edges = " + str(edges))
    clearscreen(1)
    for e in edges:
        print(e)
        othr_v_index = [idx for idx in mesh.edges[e.index].vertices if idx != v_index][0]
        connected_verts[othr_v_index] = True
        marked_edges.append(e.index)
        findConnectedVerts(othr_v_index, mesh, connected_verts, marked_edges, maxdepth=maxdepth, level=level+1)



def getaveragevertexweight():
    print("Starting getaveragevertexweight")
    for i in get_selected_vertex_data(True):
        selectedvert_data = get_selected_vertex_data(False)
        boi = selectedvert_data[i].groups
        print("Boi")
        print(boi)



def main():
    print("Main Running")
    mesh = bpy.context.object.data
        
    connected_verts = {}
    marked_edges = []
    for i in get_selected_vertex_data(True):
        connected_verts = findConnectedVerts(i, mesh, connected_verts, marked_edges, maxdepth=1)
        clearscreen(2)
        print("print connected verts??")
        print(",".join([str(v) for v in connected_verts.keys()]))
clearscreen(5)


getaveragevertexweight()