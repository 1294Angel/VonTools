"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Import Shit

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import bpy, os, json, mathutils # type: ignore
from . import von_createcontrols, von_buttoncontrols


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                ADD TO EXISTING DICTIONARY

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory

def ENUMUPDATE_gatherheirarchydata(self):

    """
    obj = bpy.context.object
    for bone in obj.data.bones:
        bpy.context.object.data.bones[bone.name].color.palette = "THEME03"
    """

    directory_path = get_directory() + "/Libraries/BoneNames"
        #OUTPUT - C:\Users\chris\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\VonTools

    dictionaryoptions = []
    itterations = -1
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


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Merge Armatures

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def gatherjsondictkeys(self,targetdict):
    json_data_list = []
    directory_path = get_directory() + "/Libraries/BoneNames"
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

def gatherspecificjsondictkeys(targetfilename):
    json_data_list = []
    directory_path = get_directory() + "/Libraries/BoneNames"
    for filename in os.listdir(directory_path):
        if filename == targetfilename:
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, 'r') as json_file:
                    data = json.load(json_file)
                    if isinstance(data, dict):
                        json_data_list.append(data)  # Store dictionaries
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
    return json_data_list

#Search If A Bone Is In A Given Dictionarty
def search_dict(dictionary, bonename):
    matches = [] # Using a list rather than just returning here so that I get a list of all possible names to rename that bone to rather than just the first
    found = False
    for data in dictionary:
        for key, value in data.items():
            if bonename in key:
                found = True
                matches.append(key)
        for key, value in data.items():
            if bonename in value:
                found = True
                matches.append(key)

    if found == True:
        return found, matches
    if found == False:
        return found, None
           
def filterbonesbyjsondictlist(selected_armatures,json_data_list,targetdict, self, isdraw):
    duplicatematches = {}
    bonestorename = {}
    undetectedbones = []
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            for bone in armature.pose.bones:
                matches = []
                bonename = bone.name
                bonename = bonename.lower()
                found, names = search_dict(targetdict, bonename) ##
                if found == True:
                    if len(names) > 1:
                        duplicatematches[bone.name] = names
                    if len(names) == 1:
                        matches.append(names)
                    if len(names) <= 0:
                        print("ERROR - search_dict - Returning TRUE + NONE - Should be TRUE + ListOfKeys or False + None")
                        continue
                if found == False:
                    secondaryfound, secondarynames = search_dict(json_data_list, bonename)
                    if secondaryfound == True:
                        if len(secondarynames) > 1:
                            duplicatematches[bone.name] = secondarynames
                        if len(secondarynames) == 1:
                            matches.append(secondarynames)
                        if len(secondarynames) <= 0:
                            print("ERROR - search_dict - Returning TRUE + NONE - Should be TRUE + ListOfKeys or False + None")
                            continue
                    if secondaryfound == False:
                        undetectedbones.append(bone.name)
                if len(matches) == 1:
                    bonestorename[bone.name] = matches[0]
        print(f"DictList_ForDrawcall -- Duplicate Matches = {duplicatematches}")
        if isdraw == False:
            rename_bones_from_dict(selected_armatures,matches,self)
    if isdraw == True:
        return duplicatematches
    if isdraw == False:
        return duplicatematches, undetectedbones, bonestorename
    


    


"""
#returns: all_matches (Dict where key is original bone name and the list is the list of options for renaming when there are more than 1) - Undetected Bones (Bones to colour to red and copy paste to the new armature) - bonestorename (Dict where bonename is the key and the list is the name to rename it to)
def filterbonesbyjsondictlist(selected_armatures,json_data_list,shouldrename,self,targetdict):
    #Gathering intial context data to allow minimal obstruction to the end user
    initialcontext = bpy.context.object.mode
    initalarmature = bpy.context.view_layer.objects.active

    all_duplicatematches = {}
    undetectedbones = []
    bonestorename = {}
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            bpy.context.view_layer.objects.active = armature
            for bone in armature.pose.bones:
                bonename = von_buttoncontrols.splitstringfromadditionalbones(bone.name.lower())
                matches = []
                #have it check through the target dict and only search ALL dicts when it cannot find it in the target dict

                for data in targetdict:
                    for key, list_data in data.items():
                        if bonename == key.lower():
                            if key not in matches:
                                bpy.context.object.data.bones[bone.name].color.palette = "THEME03"
                                matches.append(key)
                        # Check for partial match in the list data
                        elif bonename in [item.lower() for item in list_data]:
                            if key not in matches:
                                matches.append(key)
                        else:
                            for dictionarylist in json_data_list:
                                for key, list_data in dictionarylist.items():
                                    if bonename == key.lower():
                                        if key not in matches:
                                            bpy.context.object.data.bones[bone.name].color.palette = "THEME03"
                                            matches.append(key)
                                    # Check for partial match in the list data
                                    elif bonename in [item.lower() for item in list_data]:
                                        if key not in matches:
                                            matches.append(key)
                            continue
                if len(matches) == 0:
                    if bone.name not in undetectedbones:
                        undetectedbones.append(bone.name)
                else:
                    if len(matches) > 1:
                        all_duplicatematches[bone.name] = matches  # Store all matches
                    elif len(matches) == 1:
                        bonestorename[bone.name] = matches[0]
        if shouldrename == True:
            rename_bones_from_dict(selected_armatures,bonestorename,self)
    #Setting everything back to how it was prior to running the script to minimise inconvinences and cut off edge cases
    bpy.context.view_layer.objects.active = initalarmature
    bpy.ops.object.mode_set(mode=initialcontext)

    return all_duplicatematches, undetectedbones, bonestorename
"""

def rename_bones_from_dict(armaturelist, rename_dict,self):
    for armature in armaturelist:
        bpy.context.view_layer.objects.active = armature
        posebones = armature.data.bones
        for key in rename_dict:
            if key in posebones:
                bpy.context.object.data.bones[key].color.palette = "THEME03"
        
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for old_name, new_name in rename_dict.items():
            if old_name in edit_bones:
                try:
                    edit_bones[old_name].name = new_name
                except Exception as e:
                    self.report({'ERROR'}, f"Error renaming bone '{old_name}': {e}")

def setrelativescalemod(sourcearmatures,targetarmature, self):
    targetheight = targetarmature.dimensions.z
    if targetheight == 0:

        self.report({'ERROR'}, f"{targetarmature.name} HAS Z HEIGHT OF 0")
        return

    for source in sourcearmatures:
        bpy.context.view_layer.objects.active = source
        sourceheight = source.dimensions.z
        if sourceheight == 0:
            self.report({'ERROR'}, f"{source.name} - HAS Z HEIGHT OF 0")
            continue
        if targetheight == sourceheight:
            continue
        heightscale = targetheight / sourceheight

        source.scale *= heightscale
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    bpy.context.view_layer.objects.active = targetarmature


def generateextrabone(source_armatures, target_armature, self):
        
        
    def setallarmaturecontext(Mode):
        for source in source_armatures:
            bpy.context.view_layer.objects.active = source
            bpy.ops.object.mode_set(mode=Mode)
        
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode=Mode)
    addedbones = []
    foundbones = []
    setallarmaturecontext('EDIT')

    target_bones = target_armature.data.edit_bones


        

    for source in source_armatures:
        bpy.context.view_layer.objects.active = source

        source_bones = source.data.edit_bones
        
        for bone in source_bones:
            if bone.name in target_bones:
                continue
            source_bone_loop = source_bones[bone.name]
            target_bones.data.edit_bones.new(bone.name)
            target_bone = target_bones.data.edit_bones[bone.name]

            target_bone.head = source_bone_loop.head
            target_bone.tail = source_bone_loop.tail
            target_bone.roll = source_bone_loop.roll

            addedbones.append(bone.name)

            try:
                if source_bone_loop.parent:
                    if target_bones.data.edit_bones.get(source_bone_loop.parent.name):
                        target_bone.parent = target_bones.data.edit_bones.get(source_bone_loop.parent.name)
            except Exception as e:
                self.report({'ERROR'}, f"ERROR: {e}")
                continue
            else:
                continue

    
    setallarmaturecontext('OBJECT')
    print(f"Added bones = {addedbones}")
    return(addedbones)


def moveskeletalmesh(selectedarmatures, target_armature,self):
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object is not None:
                    source_armature = modifier.object
                    for selarmature in selectedarmatures:
                        selarmature_name = selarmature.name
                        if source_armature.name == selarmature_name:
                            relative_offset = obj.location - source_armature.location
                            obj.parent = target_armature
                            obj.matrix_parent_inverse = target_armature.matrix_world.inverted()

                            modifier.object = target_armature
                            obj.location = target_armature.location + relative_offset
                            
def animretargeter(target_armature,selectedarmatures,self):
    target_bones = target_armature.data.bones
    

"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""