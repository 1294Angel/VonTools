import bpy, os,json # type: ignore
from . import von_createcontrols


def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory

def gatherheirarchydata():
    directory_path = get_directory() + "/Libraries/BoneNames"
        #OUTPUT - C:\Users\chris\AppData\Roaming\Blender Foundation\Blender\4.2\scripts\addons\VonTools
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            filepath = os.path.join(directory_path, filename)
            
            with open(filepath, 'r') as json_file:
                try:
                    data = json.load(json_file)
                    print(f"\nProcessing file: {filename}")
                    
                    #If it's a dict then do X (Idiot Proofing)
                    if isinstance(data, dict):
                        iterate_over_items(data)
                    else:
                        print(f"Skipping file {filename} as it doesn't contain a valid JSON object.")
                except json.JSONDecodeError as e: # IF ALL FAILS, IDIOT PROOFING
                    print(f"Error reading {filename}: {e}")

def iterate_over_items(data):
    for key, value in data.items():
        print(f"Key: {key}, Value: {value}")