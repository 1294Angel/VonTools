#Import all needed
import bpy, re, os # type: ignore
from . import von_createcontrols 
#____________________________________________________________________________________________
#____________________________________________________________________________________________
#____________________________________________________________________________________________ 
#for object mode #Functional
def poll(compstr):
    active_object = bpy.context.mode
    if active_object == compstr:
        return True
    if active_object != compstr:
        return False

#Functional only when taking in context
def getselectedbones(context):
    bonelist = []
    bones = bpy.context.selected_pose_bones_from_active_object
    for i in bones:
        bonelist.append(i)
    return bonelist

def getselectedbonesforenum(self, context):
    constrainttypestmp = []
    enumlist = []

    addtoenum = tuple(("0","All","Target All Detected Constraints"))
    enumlist.append(addtoenum)
    

    constrainttypestmp = getboneconstraints(getselectedbones(context))
    index = 0
    for i in constrainttypestmp:        
        index = index + 1
        indexstr = str(index)
        
        i = str(i)
        
        description = "Click to alter context of these constraints on selected bones"
        
        addtoenum = tuple((indexstr, i, description))
        enumlist.append(addtoenum)
    return enumlist

def splitstringfromadditionalbones(input_string):
    match = re.search(r'(.+?)([._][lr])$', input_string, re.IGNORECASE)
    
    if match:
        return match.group(0)
    else:
        return input_string


#Functional
def colorizerig(context):
    #target_armature = bpy.context.view_layer.objects.active

    if poll("POSE") == True:
        lst_bones = getselectedbones(context)
        lst_bonenames = []
        for i in lst_bones:
            bname = i.name
            lst_bonenames.append(bname)
        
        for i in lst_bonenames:

            iendswithL = False
            iendswithR = False
            iupper = i.upper()

            if iupper.endswith("_L") or iupper.endswith(".L") == True:
                iendswithL = True
            elif i.startswith("LEFT") == True:
                iendswithL = True
            
            if iupper.endswith("_R") or iupper.endswith(".R") == True:
                iendswithR = True
            elif i.startswith("RIGHT") == True:
                iendswithL = True

            if iendswithL and iendswithR != True:
                bpy.context.object.data.bones[i].color.palette = 'THEME13'
                bpy.context.object.pose.bones[i].color.palette = 'THEME13'
            if iendswithL:
                bpy.context.object.data.bones[i].color.palette = 'THEME02'
                bpy.context.object.pose.bones[i].color.palette = 'THEME02'
            if iendswithR:
                bpy.context.object.data.bones[i].color.palette = 'THEME03'
                bpy.context.object.pose.bones[i].color.palette = 'THEME03'




#Functional
def searchforbone(selected_armature, temp_bonetofind):
    if poll("POSE") == True:
        bpy.ops.pose.select_all(action='DESELECT')
        bpy.data.objects[str(selected_armature)].data.bones[temp_bonetofind].select=True
    if poll("EDIT_ARMATURE") == True:
        bpy.ops.armature.select_all(action='DESELECT')
        bpy.data.objects[str(selected_armature)].data.bones[temp_bonetofind].select=True
#Functional
def getexistingfilesindirectories(basedirectorytosearch):
    
    FileDirectory = basedirectorytosearch / "controls"
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
    if len(constraints) > 0:
        return constraints

#Mostly Functional -- Needs to be expanded to update enum based on the selection option of another enum
def checkboneconstrainttarget(bonelist):
    selectedbones = bonelist

    for i in selectedbones:
            for con in i.constraints:
                target = con.target
                try:
                    objtarget = target.type
                except:
                    objtarget = None
                if not objtarget:
                    return None
                if objtarget == "ARMATURE":
                    return objtarget
                if objtarget != "ARMATURE":
                    return "NOTARMATURE"


def setboneconstraintspace(activearmature, selectedbones, constrainttotarget,targetspace,ownerspace):

    #Go through each bone selected
    for i in selectedbones:
        #Set the current bone's name
        bonename = i.name

        #The desired Bone
        boneToSelect = bpy.data.objects[activearmature].pose.bones[bonename].bone
        #Set as active 
        bpy.context.object.data.bones.active = boneToSelect
        #Select in viewport
        boneToSelect.select = True
        
        #Check if target of constraint is armature object or other



        for con in i.constraints:
            if con.type == constrainttotarget:   
                #Adjust each constraint on the selected bone (i) to be in Local space (need to adjust to work off of a menu str or enum later)
                bpy.context.object.pose.bones[bonename].constraints[con.name].target_space = targetspace
                bpy.context.object.pose.bones[bonename].constraints[con.name].owner_space = ownerspace
            if constrainttotarget == "All":
                #Adjust each constraint on the selected bone (i) to be in Local space (need to adjust to work off of a menu str or enum later)
                bpy.context.object.pose.bones[bonename].constraints[con.name].target_space = targetspace
                bpy.context.object.pose.bones[bonename].constraints[con.name].owner_space = ownerspace


#____________________________________________________________________________________________
#____________________________________________________________________________________________
#____________________________________________________________________________________________
