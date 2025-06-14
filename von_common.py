import bpy # type: ignore
import os, json, re, sys
from pathlib import Path # type: ignore
#-------------------------------------------------------------------------

#------ Button Controls Originally

def getboneconstraints(selectedbones):
    constraints = []
    for i in selectedbones:

        for con in i.constraints:
            
            if con.type not in constraints:
                constrainttoaddtolist = con.type
                constraints.append(constrainttoaddtolist)
    if len(constraints) > 0:
        return constraints
    
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

def getselectedbones(context):
    bonelist = []
    bones = bpy.context.selected_pose_bones_from_active_object
    for i in bones:
        bonelist.append(i)
    return bonelist

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


#------ VRC Tools Originally

def ENUMUPDATE_gatherheirarchydata(self):

    dictionaryoptions = []
    itterations = -1
    directory_path = getfolderloc()
    directory_path = directory_path / "Libraries" / "BoneNames"
    for filename in os.listdir(directory_path):

        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    #If it's a dict then do X (Idiot Proofing)
                    if isinstance(data, dict):
                        itterations = itterations + 1
                        #This is setup to update the enum
                        
                        dictionaryoptions.append((filename, filename, f"Will Add The Selected Bonename Into Your Chosen Key Within {filename}"))
                except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING NEVER REALLY TRIED THIS BEFORE
                    self.report({'ERROR'}, f"Error reading {filename}: {e}")
    return dictionaryoptions

def gatherspecificjsondictkeys(targetfilename):
    json_data_list = []
    
    # Assume getfolderloc() returns a pathlib.Path
    directory_path = getfolderloc() / "Libraries" / "BoneNames"
    
    # Ensure path exists
    if not directory_path.exists():
        print(f"Directory not found: {directory_path}")
        return []

    target_path = directory_path / targetfilename
    if not target_path.is_file():
        print(f"File not found: {target_path}")
        return []

    try:
        with open(target_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            if isinstance(data, dict):
                json_data_list.append(data)
            else:
                print(f"Warning: {targetfilename} did not contain a JSON object (dict).")
    except json.JSONDecodeError as e:
        print(f"JSON decode error in '{targetfilename}': {e}")
    except Exception as e:
        print(f"Unexpected error reading '{targetfilename}': {e}")

    return json_data_list

def filterbonesbyjsondictlist(selected_armatures,targetdict, self, isdraw):

    jsondictkeys = gatherjsondictkeys(self,targetdict)
    prioritydict = gatherspecificjsondictkeys(targetdict)
    duplicatematches = {}
    bonestorename = {}
    undetectedbones = []
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            for bone in armature.pose.bones:
                matches = []
                bonename = bone.name
                bonename = bonename.lower()
                found, names = search_dict(prioritydict[0], bonename) #Search PRIORITY dict
                if found == True:
                    if len(names) > 1:
                        duplicatematches[bone.name] = names
                    if len(names) == 1:
                        matches.append(names)
                    if len(names) <= 0:
                        continue
                if found == False:
                    
                    for dict in jsondictkeys:
                        if dict == prioritydict:
                            pass
                        secondaryfound, secondarynames = search_dict(dict, bonename) # Search Secondary Dictionaries
                        if secondaryfound == True:
                            if len(secondarynames) > 1:
                                duplicatematches[bone.name] = secondarynames
                            if len(secondarynames) == 1:
                                if len(matches) < 1:
                                    matches.append(secondarynames)
                            if len(secondarynames) <= 0:#
                                continue
                        if secondaryfound == False:
                            undetectedbones.append(bone.name)
                if len(matches) == 1:
                    for i in matches:
                        bonestorename[bone.name] = i
        if isdraw == False:
            rename_bones_from_dict(selected_armatures,bonestorename,self)
    if isdraw == True:
        return duplicatematches
    if isdraw == False:
        return duplicatematches, undetectedbones, bonestorename

def gatherjsondictkeys(self,targetdict):
    json_data_list = []

    
    directory_path = getfolderloc()
    directory_path = directory_path / "Libraries" / "BoneNames"
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
                if filename != targetdict:
                    filepath = os.path.join(directory_path, filename)
                    try:
                        with open(filepath, 'r') as json_file:
                            data = json.load(json_file)
                            if isinstance(data, dict):
                                json_data_list.append(data)  # Store dictionaries
                    except json.JSONDecodeError as e:
                        self.report({'ERROR'}, f"Error reading {filename}: {e}")
    return json_data_list

def search_dict(dictionary, bonename):
    pattern = re.compile(r"\.\d+$")
    bonename = pattern.sub("", bonename)
    matches = [] # Using a list rather than just returning here so that I get a list of all possible names to rename that bone to rather than just the first
    found = False
    spacered_bonename = normalise_string_spacers(bonename)
    print(f"spacered bonename = {spacered_bonename}")
    for key, value in dictionary.items():
        tmp_key = normalise_string_spacers(key)
        if spacered_bonename.lower() == tmp_key.lower():
            found = True
            print(f"key is {key}")
            print(found)
            matches.append(key)
            pass
        for checker in value:
            checker = normalise_string_spacers(checker)
            if spacered_bonename.lower() == checker.lower():
                found = True
                print(f"matches is {key}")
                matches.append(key)
                print("")
                print(found)
                print("")
                pass
    print("Not found")

    return found, matches if found else None

def rename_bones_from_dict(armaturelist, rename_dict,self):
    print(rename_dict)
    for armature in armaturelist:
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for old_name, new_name in rename_dict.items():
            new_name = new_name[0]       
            if old_name in edit_bones:
                if len(new_name) > 1:
                    try:
                        edit_bones[old_name].name = new_name
                    except Exception as e:
                        self.report({'ERROR'}, f"Error renaming bone '{old_name}': {e}")
                else:
                    pass
        bpy.ops.object.mode_set(mode='OBJECT')



def normalise_string_spacers(string):
    #gather the current spacer value (Aka instead of a space using _'s)
    scene = bpy.context.scene
    my_tool = scene.my_tool
    checkervalue = my_tool.stringspacerreplacer

    
    basestring = re.sub(r"[ ._]", checkervalue, string)
    match = re.match(rf"^(.*?){re.escape(checkervalue)}([lLrR])$", basestring)
    if match:
        # Remove all separators from the base part
        base = re.sub(r"[ ._]", "", match.group(1))
        suffix = f"{checkervalue}{match.group(2).lower()}"
        name = base + suffix
    else:
        name = basestring

    return name
def spaceconsole(temp):
    xx = temp
    while xx > 0:
        xx = xx -1
        print("")

def reporterror(self, e):
    self.report({'ERROR'}, f"Unexpected Error: {str(e)}")

def getselectedarmatures(context):
    return [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
    """I've been using this version, but checking selected objects seems more efficient
    [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]"""

def get_meshes_using_armature(armature_obj):
    controlled_meshes = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature_obj:
                    controlled_meshes.append(obj)
                    break
    return controlled_meshes

def get_armature_for_mesh(mesh_obj):
    for mod in mesh_obj.modifiers:
        if mod.type == 'ARMATURE' and mod.object:
            return mod.object
    return None

def stripblenderextrachars(string):
    pattern = re.compile(r"\.\d+$")
    bonename = pattern.sub("", string)
    return bonename

def getfolderloc():
    dir = Path(__file__).resolve().parent
    if str(dir) not in sys.path:
        sys.path.append(str(dir))
    return dir
#--------------------------- Enum Updates
def updateexistingboneconstraintsenum(self, context):
    getselectedbonesforenum(self, context)

def updateexistingjsondictonaries(self, context):
    #FUNCTIONAL
    return ENUMUPDATE_gatherheirarchydata(self)
def updatejsonkeyoptions(self, context):

    directory_path = getfolderloc()
    directory_path = directory_path / "Libraries" / "BoneNames"
    parentenumoption = self.jsondictionaryoptions_enum
    directory_path = os.path.join(directory_path, parentenumoption)

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The file {directory_path} does not exist.")
    
    with open(directory_path, 'r') as file:
        data = json.load(file)

    iterations = -1
    enum_items = []
    for key in data.keys():
        iterations = iterations + 1
        enum_items.append((key, key, f"Description for {key}"))

    return enum_items

def updatebonestandarizationoptions(self, context):
    all_matches = {}
    my_tool = context.scene.my_tool
    selected_dict = my_tool.AvalibleNamingConventions
    targetdict = gatherspecificjsondictkeys(selected_dict)
    selected_armatures = getselectedarmatures(context)
    all_matches = filterbonesbyjsondictlist(selected_armatures, selected_dict, self, True)
    return all_matches


def updatetargetspaceenumlist(self, context):
    factor = checkboneconstrainttarget(getselectedbones(context))
    enumlist = []
    if factor == "ARMATURE":
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description"), ("4", "POSE", "Description"), ("5", "LOCAL_WITH_PARENT", "Description"), ("6", "LOCAL_OWNER_ORIENT", "Description")]
        return enumlist
    if factor != "ARMATURE":
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description")]
        return enumlist        

def updateavaliblenamingconventions(self, context):
    namingconventions = []
    directory_path = getfolderloc()
    directory_path = directory_path / "Libraries" / "BoneNames"

    if not directory_path.exists():
        print(f"[ERROR] Path does not exist: {directory_path}")
        return namingconventions

    for filename in os.listdir(directory_path):
        filename = str(filename)
        namingconventions.append((filename, filename, "This is a filename"))

    return namingconventions

def updatestringspacersoptions(self,context):
    stringspacers = [("_", "_", "Turns all spaces and .'s into _'s"), (".", ".", "Turns all spaces and _'s into .'s"), (" ", " ", "Turns all underscores and .'s into spaces's")]
    return stringspacers



#-----------------------------------------------------------------------
class MySettings(bpy.types.PropertyGroup):
#--------------
  
    ExistingBoneConstraints_enum : bpy.props.EnumProperty(
        name = "",
        description = "",
        items = getselectedbonesforenum,
        update = updateexistingboneconstraintsenum
    ) # type: ignore

    targetspace_enum: bpy.props.EnumProperty(
        name = "Target Space - ",
        description = "The Setting Target Space will be set to",   
        items = updatetargetspaceenumlist,
        update = updatetargetspaceenumlist
    ) # type: ignore
#--------------
    jsondictionaryoptions_enum : bpy.props.EnumProperty(
        name = "Avalible Json Dictionaries - ",
        description = "Choose an option",
        items = updateexistingjsondictonaries,
        update = lambda self, context: context.scene.my_settings.option_enum.update(context)
    ) # type: ignore
    
    jsondictionarykeyoptions_enum: bpy.props.EnumProperty(
        name="Avalible Keys - ",
        description="Choose an option",
        items=updatejsonkeyoptions
    ) # type: ignore

    vrc_tool_options: bpy.props.StringProperty(
        name="TempName",
        description="Store serialized dictionary as a JSON string",
        default="{}"
    ) # type: ignore

#---------------

    definedroot: bpy.props.StringProperty(
            name="Root Bone Name",
            description="What is the name of the root bone?",
            default="Root"
        ) # type: ignore

    posebonelimit: bpy.props.IntProperty(
        name="Pose Bone Limit",
        description="Maximum number of exportable deform bones allowed",
        default=0
    ) # type: ignore
#--------------
    AvalibleNamingConventions: bpy.props.EnumProperty(
        name = "AvalibleNamingConventions",
        description = "Choose an option from the list to standardize naming conventions",
        items = updateavaliblenamingconventions,
    ) # type: ignore
#--------------

    stringspacerreplacer : bpy.props.EnumProperty(
        name = "Spacer Replacement Options",
        description = "Choose what to set your spacers as (eg: _ or .)",
        items = [("_", "_", "Turns all spaces and .'s into _'s"), (".", ".", "Turns all spaces and _'s into .'s"), (" ", " ", "Turns all underscores and .'s into spaces's")],
        update = updatestringspacersoptions
    ) # type: ignore


#--------------

    def get_vrc_tool_options(self):
        """Deserialize the JSON string into a dictionary."""
        return json.loads(self.vrc_tool_options)
    
    def set_vrc_tool_options(self, value):
        """Serialize a dictionary into a JSON string."""
        self.vrc_tool_options = json.dumps(value)
#--------------

    pass