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
                        issues[armature.name]["CyclicConstraint"].add(f"{bone.name} contains a cyclic constraint: {constraint.name}")
        bpy.ops.object.mode_set(mode='OBJECT')
    return issues

def checkweightinfluences(maxinfluences,issues):
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers:
                if modifier.type == 'ARMATURE' and modifier.object is not None:
                    mesh = obj.data
                    for vert in mesh.verticies:
                        if len(vert.groups) > maxinfluences:
                            issues["AbundantInfluences"] = "Abundant Influences: {obj.name} contains too many influences."
    return issues

def findemptyvertexgroups(skeletalmesh, issues):
    for sk in skeletalmesh:
        for vg in sk.vertex_groups:
            used = False
            for vertex in sk.data.vertices:
                for group in vertex.groups:
                    if group.group == vg.index:
                        used = True
                        break
                if used:
                    break
            if not used:
                issues[sk.name]["Empty Vertex Groups"].add(vg.name)
    return issues

def find_unweighted_vertices(skeletalmesh, issues):
    for sk in skeletalmesh:
        unweighted = 0
        for vertex in sk.data.vertices:
            if not vertex.groups:
                unweighted = unweighted + 1
        if unweighted >= 1:
            issues[sk.name]["Unweighted Verts"].add(unweighted)
    return issues

def find_non_deform_weighted_bones(skeletalmesh, issues):
    for sk in skeletalmesh:
        armature = von_devtools.get_armature_for_mesh(sk)
        if not armature:
            continue

        weighted_bones = {vg.name for vg in sk.vertex_groups}

        for bone in armature.data.bones:
            if not bone.use_deform and bone.name in weighted_bones:
                issues[sk.name]["Non-Deform Bones Weighted"].add(bone.name)

    return issues

def check_multiple_armatures(skeletalmesh, issues):
    for sk in skeletalmesh:
        modifiervolume = 0
        for m in sk.modifiers:
            if m.type == 'ARMATURE':
                modifiervolume = modifiervolume + 1
    if modifiervolume == 0:
        issues[sk.name]["Armature Modifier Issue"].add("No Armature Modifier on skeletal mesh")#
    if modifiervolume >= 2:
        issues[sk.name]["Armature Modifier Issue"].add("Too many armature modifiers on skeletal mesh")#
    return issues

