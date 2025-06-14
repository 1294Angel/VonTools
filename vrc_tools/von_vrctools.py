"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Import Shit

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

import bpy, os, json, mathutils # type: ignore
from .. import von_createcontrols
from pathlib import Path
from .. import von_devtools
from .. von_common import gatherspecificjsondictkeys, filterbonesbyjsondictlist, MySettings, gatherjsondictkeys, rename_bones_from_dict
"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                ADD TO EXISTING DICTIONARY

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
def get_directory():
    addon_directory = os.path.dirname(__file__)
    return addon_directory


"""
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                Merge Armatures

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""



    



def rename_bones_from_dict(armaturelist, rename_dict,self):
    for armature in armaturelist:
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