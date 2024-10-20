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
def standardizeheirarchynames(context):
    print("--------------------------------------------------------------")
    print("STARTING STANDARIZATION OF HEIRARCHIES")
    selected_objects = bpy.context.selected_objects
    selected_armatures = [obj for obj in selected_objects if obj.type == 'ARMATURE']
    directory_path = get_directory() + "/Libraries/BoneNames"
    detectedbones = []
    json_data_list = []
    directory_path = get_directory() + "/Libraries/BoneNames"
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, 'r') as json_file:
                    print(f"{filepath} Opened successfully")
                    data = json.load(json_file)
                    if isinstance(data, dict):
                        json_data_list.append(data)  # Store dictionaries
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")

    for armature in selected_armatures:
        for bone in armature.pose.bones:
            bonefound = False
            bonename = bone.name.lower()

            
            for data in json_data_list:
                for key, list_data in data.items():
                    if bone.name == key:
                        print(f"Bone is key = {key}")
                        bpy.context.object.data.bones[bone.name].color.palette = "DEFAULT"
                        detectedbones.append(bone.name)
                        bonefound = True
                        break

                    
                    elif bonename in list_data:
                        bone.name = key
                        print(f"Bone is in list - Renaming to - {key}")
                        detectedbones.append(bone.name)
                        bpy.context.object.data.bones[bone.name].color.palette = "DEFAULT"
                        bonefound = True
                        break
                if bonefound:
                    break
            if not bonefound:
                print(f"{bone.name} - NOT IDENTIFIED")
                bpy.context.object.data.bones[bone.name].color.palette = "THEME01"
    print("ENDING STANDARDIZATION OF HEIRARCHIES")
    print("--------------------------------------------------------------")







"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""