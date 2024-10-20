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
def filterbonesbyjsondictlist(selected_armatures,json_data_list):
    all_matches = {}
    undetectedbones = []
    bonestorename = {}
    if len(selected_armatures) > 0:
        for armature in selected_armatures:
            for bone in armature.pose.bones:
                bonename = bone.name.lower()
                print(f"Bonename == {bonename}")
                matches = []
                for data in json_data_list:
                    for key, list_data in data.items():
                        if bone.name == key:
                            print("")
                            print(f"{bone.name} Match FOUND -------------- {key}")
                            print("")
                            matches.append(key)
                        elif bonename in list_data:
                            for item in matches:
                                if item != key:
                                    matches.append(key)
                if len(matches) > 0:
                    print("")
                    print(f"Bone Identified {bone.name}")
                    print("")
                    if len(matches) >= 2:
                        all_matches[bone.name] = item
                    elif len(matches) == 1:
                        if bone.name != key:
                            bonestorename[bone.name] = matches[0]
                else:
                    undetectedbones.append(bone.name)
                print(f"Matches = {matches}")
    print(f"All Matches = {all_matches}")
    print(f"Bones To Rename = {bonestorename}")
    return all_matches, undetectedbones, bonestorename


def rename_bones_from_dict(selectedarmatures, rename_dict):
    for armature in selectedarmatures:
        armature = bpy.data.objects.get(armature.name)
        if armature is not None and armature.type == 'ARMATURE':
            bones = armature.data.bones
            for old_bone_name, new_bone_name in rename_dict.items():
                if old_bone_name in bones:
                    bones[old_bone_name].name = new_bone_name
                    bpy.context.object.data.bones[new_bone_name].color.palette = "THEME03"
                    print(f"Renamed bone '{old_bone_name}' to '{new_bone_name}'")
                else:
                    print(f"Bone '{old_bone_name}' not found in armature '{armature.name}'")
        else:
            print(f"Armature '{armature.name}' not found or is not an armature")






"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""