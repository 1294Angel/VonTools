import bpy # type: ignore


# ------------------------------------------------------------------------
#    
# ------------------------------------------------------------------------

def checkbones(armaturestocheck, issues):
    for armature in armaturestocheck:
        bpy.ops.object.mode_set(mode='POSE')
        for bone in armature.pose.bones:
            if bone.parent == None:
                issues[armature.name]["OrphanBones"] = {bone.name}

            elif bone.parent == bone:
                issues[armature.name]["CyclicDependancy"] = {armature.name},{bone.name}
    return issues

def checkconstraints(armaturetocheck, issues):
    bpy.ops.object.mode_set(mode='POSE')

    for bone in armaturetocheck.pose.bones:
        for constraint in bone.constraints:
            if constraint.type == 'IK' and len(bone.constraints) > 1:
                issues["MultipleIkConstraints"] = f"Multiple Constraints: {bone.name} has multiple IK constraints"
            if constraint.target == None:
                issues["EmptyConstraint"] = f"Empty Constraints: {bone.name} contains an empty constraint: {constraint.name}"
            if constraint.target == bone:
                issues["CyclicConstraint"] = f"Cyclic Constraint: {bone.name} contains a cyclic constraint: {constraint.name}"
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



