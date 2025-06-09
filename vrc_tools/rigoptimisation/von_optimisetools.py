import bpy # type: ignore
from ... import von_devtools

# ------------------------------------------------------------------------
#    
# ------------------------------------------------------------------------

def cullorphans(armaturestocheck,definedroot):
    for armature in armaturestocheck:
        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = armature.data.edit_bones
        for bone in edit_bones:
            if bone.parent == None:
                if bone.name != definedroot:
                    edit_bones.remove(edit_bones[bone.name])
        bpy.ops.object.mode_set(mode='OBJECT')


def checkbones(armaturestocheck, issues, definedroot, posebonelimit):
    for armature in armaturestocheck:
        bpy.ops.object.mode_set(mode='POSE')
        num_pose_bones = sum(1 for pbone in armature.pose.bones if pbone.bone.use_deform)
        if num_pose_bones > posebonelimit:
            issues[armature.name]["BoneLimitReached"].add(f"Contains {num_pose_bones} bones")
        for bone in armature.pose.bones:
            if bone.parent == None:
                if bone.name != definedroot:
                    issues[armature.name]["OrphanBones"].add(bone.name)
            elif bone.parent == bone:
                issues[armature.name]["CyclicDependancy"].add(bone.name)
        bpy.ops.object.mode_set(mode='OBJECT')
    return issues

def checkconstraints(armaturetocheck, issues):
    bpy.ops.object.mode_set(mode='OBJECT')
    for armature in armaturetocheck:
        bpy.ops.object.mode_set(mode='POSE')
        for bone in armature.pose.bones:
            if bone:
                for constraint in bone.constraints:
                    if constraint.type == 'IK' and len(bone.constraints) > 1:
                        issues[armature.name]["MultipleIkConstraints"].add(bone.name)
                    if constraint.target == None:
                        issues[armature.name]["EmptyConstraint"].add(f"{bone.name} contains an empty constraint: {constraint.name}")
                    if constraint.target == bone:
                        issues["CyclicConstraint"].add(f"{bone.name} contains a cyclic constraint: {constraint.name}")
        bpy.ops.object.mode_set(mode='OBJECT')
    return issues

def checkweightinfluences(maxinfluences,issues):
    bpy.ops.object.mode_set(mode='OBJECT')
    issues = []
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object is not None:
                    mesh = obj.data
                    for vert in mesh.verticies:
                        if len(vert.groups) > maxinfluences:
                            issues["AbundantInfluences"] = "Abundant Influences: {obj.name} contains too many influences."
    return issues




def stresstestrig(armatures, testaxis):
    bpy.ops.object.mode_set(mode='POSE')
    for armature in armatures:
        for bone in armature.pose.bones:
            bone.rotation_euler.testaxis += 0.5
    bpy.ops.object.mode_set(mode='OBJECT')



