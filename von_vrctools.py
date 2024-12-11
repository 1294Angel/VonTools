"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Import Shit

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import bpy, os,json # type: ignore
from . import von_createcontrols, von_buttoncontrols


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                ADD TO EXISTING DICTIONARY

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory

def ENUMUPDATE_gatherheirarchydata():

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

                    else:
                        print(f"Skipping file {filename} as it doesn't contain a valid JSON object.")
                except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING NEVER REALLY TRIED THIS BEFORE
                    print(f"Error reading {filename}: {e}")
    #print(f"The Options for the Enum Will be: {dictionaryoptions}")
    return dictionaryoptions


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Merge Armatures

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def gatherjsondictkeys():
    json_data_list = []
    directory_path = get_directory() + "/Libraries/BoneNames"
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, 'r') as json_file:
                    data = json.load(json_file)
                    if isinstance(data, dict):
                        print(json_file)
                        json_data_list.append(data)  # Store dictionaries
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")
    return json_data_list

def filterbonesbyjsondictlist_fordrawcall(selected_armatures,json_data_list):
    all_duplicatematches = {}
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            for bone in armature.pose.bones:
                bonename = von_buttoncontrols.splitstringfromadditionalbones(bone.name.lower())
                matches = []
                for data in json_data_list:
                    for key, list_data in data.items():
                        if bonename == key.lower():
                            if key not in matches:
                                matches.append(key)
                        elif bonename in [item.lower() for item in list_data]:
                            if key not in matches:
                                matches.append(key)
                        else:
                            continue
                else:
                    if len(matches) > 1:
                        all_duplicatematches[bone.name] = matches  # Store all matches
    return all_duplicatematches

#returns: all_matches (Dict where key is original bone name and the list is the list of options for renaming when there are more than 1) - Undetected Bones (Bones to colour to red and copy paste to the new armature) - bonestorename (Dict where bonename is the key and the list is the name to rename it to)
def filterbonesbyjsondictlist(selected_armatures,json_data_list,shouldrename):
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
                for data in json_data_list:
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
            rename_bones_from_dict(selected_armatures,bonestorename)
    von_createcontrols.spaceconsole(2)
    print(f"All Matches = {all_duplicatematches}")
    print(f"Undetected Bones = {undetectedbones}")
    print(f"Bones To Rename = {bonestorename}")
    von_createcontrols.spaceconsole(2)

    #Setting everything back to how it was prior to running the script to minimise inconvinences and cut off edge cases
    bpy.context.view_layer.objects.active = initalarmature
    bpy.ops.object.mode_set(mode=initialcontext)

    return all_duplicatematches, undetectedbones, bonestorename


def rename_bones_from_dict(armaturelist, rename_dict):
    for armature in armaturelist:
        bpy.context.view_layer.objects.active = armature
        print(armature.name)
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
                    print(f"Error renaming bone '{old_name}': {e}")
            else:
                print(f"Bone '{old_name}' not found in armature '{armature.name}'.")

def generateextrabone(source_armatures, target_armature, bonelist):
    def setallarmaturecontext(Mode):
        for source in source_armatures:
            bpy.context.view_layer.objects.active = source
            bpy.ops.object.mode_set(mode=Mode)
        
        bpy.context.view_layer.objects.active = target_armature
        bpy.ops.object.mode_set(mode=Mode)
    print("BONELIST IS ")
    print(bonelist)
    addedbones = []
    setallarmaturecontext('EDIT')

    target_bones = target_armature.data.edit_bones


        

    for source in source_armatures:
        bpy.context.view_layer.objects.active = source

        source_bones = source.data.edit_bones
        print(f"Source bones = {source_bones}")

        for bone in bonelist:
            if bone not in source_bones:
                print(f"{bone} Not Detected In Source")
                continue
            source_bone_loop = source_bones[bone]
            print(f"Source Bone Loop = {source_bone_loop}")

            if bone not in target_armature.data.bones:
                print(f"Bone is {bone}")
                target_bones.data.edit_bones.new(bone)
                addedbones.append(bone)
                target_bone = target_bones.data.edit_bones[bone]

                target_bone.head = source_bone_loop.head
                target_bone.tail = source_bone_loop.tail
                target_bone.roll = source_bone_loop.roll

                try:
                    if source_bone_loop.parent:
                        if target_bones.data.edit_bones.get(source_bone_loop.parent.name):
                            target_bone.parent = target_bones.data.edit_bones.get(source_bone_loop.parent.name)
                        else:
                            print("Parent Bone Doesn't Exist Bro")
                except Exception as e:
                    print(f"ERROR 129: {e}")
                    continue
            else:
                continue


    setallarmaturecontext('POSE')
    for i in target_bones:
        if i in addedbones:
            bpy.context.object.data.bones[i].color.palette = "THEME04"
        else:
            bpy.context.object.data.bones[i].color.palette = "THEME03"
    setallarmaturecontext('OBJECT')








"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""