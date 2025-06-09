"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Import Shit

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import bpy, os, json, mathutils # type: ignore

"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                ADD TO EXISTING DICTIONARY

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory

def ENUMUPDATE_gatherheirarchydata(self):

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
    #print(f"DEBUG:Targetfilename is - {targetfilename}")
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
                #self.report({'ERROR'}, f"Error reading {filename}: {e}")
                print(f"Error reading {filename}: {e}")
    return json_data_list

#Search If A Bone Is In A Given Dictionarty
def search_dict(dictionary, bonename):
    matches = [] # Using a list rather than just returning here so that I get a list of all possible names to rename that bone to rather than just the first
    found = False
    for key, value in dictionary.items():
        if bonename == key:
            found = True
            matches.append(key)
        if bonename in value:
            found = True
            matches.append(key)

    return found, matches if found else None
           
def filterbonesbyjsondictlist(selected_armatures,targetdict, self, isdraw):
    jsondictkeys = gatherjsondictkeys(self,targetdict)
    prioritydict = gatherspecificjsondictkeys(targetdict)
    #print(f"DEBUG:prioritydict is - {prioritydict}")
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
    



def rename_bones_from_dict(armaturelist, rename_dict,self):
    for armature in armaturelist:
        #bpy.context.view_layer.objects.active = armature
        #posebones = armature.data.bones
        #for key in rename_dict:
        #    if key in posebones:
        #        bpy.context.object.data.bones[key].color.palette = "THEME03"
        
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for old_name, new_name in rename_dict.items():
            if old_name in edit_bones:
                try:
                    edit_bones[old_name].name = new_name[0]
                except Exception as e:
                    self.report({'ERROR'}, f"Error renaming bone '{old_name}': {e}")
        bpy.ops.object.mode_set(mode='OBJECT')

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
                            

    

"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Something Else

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""