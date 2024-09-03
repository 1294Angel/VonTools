import bpy # type: ignore
context=bpy.context
pbone = context.active_pose_bone

def clear(len):
    for i in range(len):
        print("")

clear(5)

#Go through each bone selected
for i in context.selected_pose_bones_from_active_object:
    clear(3)
    #Set the current bone's name
    bonename = i.name
    print("Bonename = " + bonename)

    # TRYNA GET BONE SELECTION WORKING

        #The desired Bone
    boneToSelect = bpy.data.objects["Armature"].pose.bones[bonename].bone
        #Set as active 
    bpy.context.object.data.bones.active = boneToSelect
        #Select in viewport
    boneToSelect.select = True
    print("i is selected?" + boneToSelect.name)
    print("CONSTRAINTS =" + pbone.constraints)
    # END OF TRYNA GET BONE SELECTION WORKING



    
    #For each constraint in the current bone (i)
    for con in i.constraints:
        #Check it is reading the constraints correctly (Working)
        print("Con.Type = " + con.type)
        constraintname = str(con.name)
        print("Constraint Name? = " + constraintname)
            
        #Adjust each constraint on the selected bone (i) to be in Local space (need to adjust to work off of a menu str or enum later)
        bpy.context.object.pose.bones[bonename].constraints[constraintname].target_space = 'LOCAL'
        bpy.context.object.pose.bones[bonename].constraints[constraintname].owner_space = 'LOCAL'
        print("set to local space")
    