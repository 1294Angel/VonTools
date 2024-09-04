#Import all needed
import bpy # type: ignore
import os
from . import von_createcontrols
from .von_createcontrols import *    
#____________________________________________________________________________________________
#____________________________________________________________________________________________
#____________________________________________________________________________________________ 
#for object mode #Functional
def poll(compstr):
    active_object = bpy.context.mode
    if active_object == compstr:
        bool = True
        print(active_object + " --- " + "True")
        return bool
    if active_object != compstr:
        bool = False
        print(active_object + " --- " + "False")
        return bool
#Functional only when taking in context
def getselectedbones(context):
    bonelist = []
    bones = bpy.context.selected_pose_bones_from_active_object
    for i in bones:
        print(i.name)
        bonelist.append(i)
    return bonelist

def getselectedbonesforenum(self, context):
    print("Selected bones for enum")
    constrainttypestmp = []
    enumlist = []
    print(enumlist)

    addtoenum = tuple(("0","All","Target All Detected Constraints"))
    enumlist.append(addtoenum)

    constrainttypestmp = getboneconstraints(getselectedbones(context))
    
    index = 0
    for i in constrainttypestmp:
        toadd = ()
        
        index = index + 1
        indexstr = str(index)
        
        i = str(i)
        
        description = "Click to alter context of these constraints on selected bones"
        
        addtoenum = tuple((indexstr, i, description))
        enumlist.append(addtoenum)
        print(enumlist)
    return enumlist
    
        

#Functional
def colorizerig(context):
    if poll("POSE") == True:
        lst_bonenames = getselectedbones(context)
        print(lst_bonenames)
        for i in lst_bonenames:
            if i.endswith("_L") and i.endswith ("_R") != True:
                print("Else --")
                print(i)
                bpy.context.object.data.bones[i].color.palette = 'THEME13'
                bpy.context.object.pose.bones[i].color.palette = 'THEME13'
            if i.endswith("_L"):
                print("L ---")
                print(i)
                bpy.context.object.data.bones[i].color.palette = 'THEME02'
                bpy.context.object.pose.bones[i].color.palette = 'THEME02'


            if i.endswith("_R"):
                print("R ---")
                print(i)
                bpy.context.object.data.bones[i].color.palette = 'THEME03'
                bpy.context.object.pose.bones[i].color.palette = 'THEME03'
            
            else:
                print("Error-04-ColorizeRig-NameNotIdentifying")
    else:
        print("Error-3-ColorizeRig-PollNotEqual")

#Functional
def searchforbone(selected_armature, temp_bonetofind):
    if poll("POSE") == True:
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects[str(selected_armature)].data.bones[temp_bonetofind].select=True
    if poll("EDIT_ARMATURE") == True:
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.data.objects[str(selected_armature)].data.bones[temp_bonetofind].select=True
    else:
        print("Error-4-SearchForBone-PollNotEqual")
#Functional
def getexistingfilesindirectories(basedirectorytosearch):
    
    FileDirectory = str(basedirectorytosearch)+"//"+"controls"
    totallist = os.listdir(FileDirectory)
    return totallist
    #[['FUCKYEAH.json', 'Suzanne.json'], ['Curious.json']]

#This will be used to populate the Enum
def getboneconstraints(selectedbones):
    constraints = []
    for i in selectedbones:

        for con in i.constraints:
            
            if con.type not in constraints:
                constrainttoaddtolist = con.type
                constraints.append(constrainttoaddtolist)
                print("Added " + constrainttoaddtolist + " To Constraints List")
    if len(constraints) > 0:
        return constraints

def setboneconstraintspace(activearmature, selectedbones, constrainttotarget,targetspace,ownerspace):

    spaceconsole(5)
    print(f"Active Armature = {activearmature}  -- Selected Bones = {selectedbones}  -- Constraint To Target = {constrainttotarget}  -- Targetspace = {targetspace}  -- Ownerspace = {ownerspace}")


    #Go through each bone selected
    for i in selectedbones:
        #Set the current bone's name
        bonename = i.name
        print("Bonename = " + bonename)

        #The desired Bone
        boneToSelect = bpy.data.objects[activearmature].pose.bones[bonename].bone
        spaceconsole(2)
        print(f"Bone to select = {boneToSelect}")
        #Set as active 
        bpy.context.object.data.bones.active = boneToSelect
        #Select in viewport
        boneToSelect.select = True
        spaceconsole(1)
        print("i = " + i.name)
        print("i is selected? = " + bpy.context.active_pose_bone.name)

        for con in i.constraints:
            bpy.context.object.data.bones.active = boneToSelect
            if constrainttotarget == "all" or "All":
                print("Contraint To Target is All")
                #Adjust each constraint on the selected bone (i) to be in Local space (need to adjust to work off of a menu str or enum later)
                bpy.context.object.pose.bones[bonename].constraints[con.name].target_space = targetspace
                bpy.context.object.pose.bones[bonename].constraints[con.name].owner_space = ownerspace
                #confirm all is working
                print("set target to " + targetspace + " space")
                print("set owner to " + ownerspace + " space")
            elif con.type == constrainttotarget: 
                print ("Constraint To Target is: " + str(constrainttotarget))               
                #Adjust each constraint on the selected bone (i) to be in Local space (need to adjust to work off of a menu str or enum later)
                bpy.context.object.pose.bones[bonename].constraints[con.name].target_space = targetspace
                bpy.context.object.pose.bones[bonename].constraints[con.name].owner_space = ownerspace
                #confirm all is working
                print("set target to " + targetspace + " space")
                print("set owner to " + ownerspace + " space")
        
#____________________________________________________________________________________________
#____________________________________________________________________________________________
#____________________________________________________________________________________________
