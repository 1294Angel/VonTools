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

#returns: all_matches (Dict where key is original bone name and the list is the list of options for renaming when there are more than 1) - Undetected Bones (Bones to colour to red and copy paste to the new armature) - bonestorename (Dict where bonename is the key and the list is the name to rename it to)
def filterbonesbyjsondictlist(selected_armatures,json_data_list,shouldrename):
    all_duplicatematches = {}
    undetectedbones = []
    bonestorename = {}
    print(f"Selected Armatures ================= {selected_armatures}")
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            for bone in armature.pose.bones:
                bonename = von_buttoncontrols.splitstringfromadditionalbones(bone.name.lower())
                matches = []
                print(f"Searching {bonename}")
                for data in json_data_list:
                    for key, list_data in data.items():
                        if bonename == key.lower():
                            if key not in matches:
                                print(f"{bone.name} = No Change")
                                bpy.context.object.data.bones[bone.name].color.palette = "THEME03"
                        # Check for partial match in the list data
                        elif bonename in [item.lower() for item in list_data]:
                            if key not in matches:
                                print(f"{bone.name} found in list_data of {key}")
                                print("Adding to matches")
                                matches.append(key)
                            else:
                                print(f"{bonename} contained in matches")
                        else:
                            continue
                if len(matches) == 0:
                    undetectedbones.append(bone.name)
                else:
                    if len(matches) > 1:
                        print(f"{armature.name} bone {bone.name} identified with more than 1 match")
                        all_duplicatematches[bone.name] = matches  # Store all matches
                    elif len(matches) == 1:
                        bonestorename[bone.name] = matches[0]
            if shouldrename == True:
                rename_bones_from_dict(armature,bonestorename)
    print(f"All Matches = {all_duplicatematches}")
    print(f"Undetected Bones = {undetectedbones}")
    print(f"Bones To Rename = {bonestorename}")
    print("")
    return all_duplicatematches, undetectedbones, bonestorename


def rename_bones_from_dict(armature, rename_dict):
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
                print(f"Renamed bone '{old_name}' to '{new_name}'.")
            except Exception as e:
                print(f"Error renaming bone '{old_name}': {e}")
        else:
            print(f"Bone '{old_name}' not found in armature '{armature.name}'.")
    


    bpy.ops.object.mode_set(mode='OBJECT')







"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""