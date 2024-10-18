"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Import Shit

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import bpy, os,json # type: ignore
from . import von_createcontrols


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Merge Armatures

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

#GetFilepath Of Library
def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory

#Get The Data Out Of Each .json Dictionary In The Library
def gatherheirarchydata(selectedheirarchy,selectedbone):
    directory_path = get_directory() + "/Libraries/BoneNames"
        #OUTPUT - C:\Users\chris\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\VonTools

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            with open(filepath, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    #If it's a dict then do X (Idiot Proofing)
                    if isinstance(data, dict):
                        iterate_overheirarchydata(data,selectedbone)
                    else:
                        print(f"Skipping file {filename} as it doesn't contain a valid JSON object.")
                except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING
                    print(f"Error reading {filename}: {e}")

#What Should Be Done To Each Key/UnityName In The Dictionary
def iterate_overheirarchydata(data, bonename):

    for unityname, possiblenames in data.items():
        for name in possiblenames:
            if bonename == name:
                print(f"Name Matches! : {name}")
    



"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""