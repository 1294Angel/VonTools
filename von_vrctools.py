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
    obj = bpy.context.object
    directory_path = get_directory()
    undetectedbones = []
    #For each armature and For each bone, check the name against EVERY key, and EVERY item in each list within each key - If it is identified then rename the bone to the key - If it is not, colour it red
    for armature in obj:
        for bone in obj.bones:
            for filename in os.listdir(directory_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(directory_path, filename)
                    with open(filepath, 'r') as json_file:
                        try:
                            data = json.load(json_file)
                            #If it's a dict then do X (Idiot Proofing)
                            if isinstance(data, dict):
                                for key, list in data:
                                    if bone.name == key:
                                        print(f"Bone is key = {key}")
                                    else:
                                        for item in list:
                                            if item == bone.name:
                                                bone.name = key
                                                print(f"Bone is in list - Attempting to rename to - {key} - Bone is now called - {bone.name} ")
                                            elif item != bone.name:
                                                print(f"{bone.name} - NOT IDENTIFIED")
                                                bpy.context.object.data.bones[bone.name].color.palette = "THEME03"
                                                undetectedbones.append(bone.name)
                        except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING -- Seems to work? Copy pasted from "ENUMUPDATE_gatherheirarchydata()"
                            print(f"Error reading {filename}: {e}")






"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""