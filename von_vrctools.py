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

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    #If it's a dict then do X (Idiot Proofing)
                    if isinstance(data, dict):
                        """
                        This will go through each individual file, works for me so far - 
                        I think the best thing to do is create the ability to ADD to the library with ease, and then to work on the merging portion of the script, so this might get duplicated but oh well
                        """
                        dictionaryoptions.append(filename)

                    else:
                        print(f"Skipping file {filename} as it doesn't contain a valid JSON object.")
                except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING NEVER REALLY TRIED THIS BEFORE
                    print(f"Error reading {filename}: {e}")
    print(f"The Options for the Enum Will be: {dictionaryoptions}")
    return dictionaryoptions


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Merge Armatures

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

"""
This is entirely wrong and need to be remade so that things can be easilly added.

def iterate_overheirarchydata(data,context):
    obj = bpy.context.object
    bones = obj.data.bones

    for basename in bones.name:
        print(f"Bonename is {basename}")
        basename = basename.lower()
        for unityname, possiblenames in data.items():
            for name in possiblenames:
                if bones == name:
                    basename = unityname
                    bpy.context.object.data.bones[basename].color.palette = "THEME03"
                    von_buttoncontrols.spaceconsole(3)
                    print(f"Bone {basename} has been found")
                    von_buttoncontrols.spaceconsole(3)
"""




"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""