
# ------------------------------------------------------------------------
#    Addon Info
# ------------------------------------------------------------------------


import bpy, sys, os, re, json # type: ignore
from pathlib import Path
from collections import defaultdict
from bpy.props import (StringProperty, # type: ignore
                       BoolProperty,
                       IntProperty,
                       FloatProperty, 
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from .vrc_tools import von_vrctools
from .vrc_tools.rigoptimisation import von_optimisetools
from . import von_createcontrols, von_buttoncontrols
from .von_common import *

# ------------------------------------------------------------------------
#    Popout Submenu's
# ------------------------------------------------------------------------

class VonPanel_RiggingTools__Submenu_BoneSearch(bpy.types.Operator):
    bl_idname = "von.popoutpanelbonesearch"
    bl_label = "Bone Search"
    

    text : bpy.props.StringProperty(
        name="Enter Text", default=""
        ) # type: ignore
    def execute(self, context):
        text = self.text
        armaturename=bpy.context.selected_objects
        von_buttoncontrols.searchforbone(bpy.context.selected_objects[0].name, text)
        return {'FINISHED'}
    def invoke(self, context, event):   
        return context.window_manager.invoke_props_dialog(self)

class VonPanel_RiggingTools_Submenu_MassSetBoneConstraintSpace(bpy.types.Operator):
    bl_idname = "von.masssetboneconstraintspace"
    bl_label = "Mass Set Constraint Space"

    ownerspace_enum: EnumProperty(
        name = "Owner Space - ",
        description = "The Setting Owner Space will be set to",   
        items = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description"), ("4", "POSE", "Description"), ("5", "LOCAL_WITH_PARENT", "Description")]
    ) # type: ignore

 
    def execute(self, context):
        scene = context.scene
        mytool=scene.my_tool

        activearmature = bpy.context.selected_objects[0].name
        spacebruhs = ("LOCAL", "WORLD", "CUSTOM","POSE","LOCAL_WITH_PARENT","LOCAL_OWNER_ORIENT")
        constraints = von_buttoncontrols.getselectedbonesforenum(self, context)
        selectedbones = von_buttoncontrols.getselectedbones(context)

        constraintchosen = int(mytool.ExistingBoneConstraints_enum)
        targetspacechosen = int(mytool.targetspace_enum)
        ownerspacechosen = int(self.ownerspace_enum)

        targetspacechosen = targetspacechosen - 1
        ownerspacechosen = ownerspacechosen - 1
        ownerspace = spacebruhs[ownerspacechosen]
        targetspace = spacebruhs[targetspacechosen]
        constraint = constraints[constraintchosen][1]
        try:
            von_buttoncontrols.setboneconstraintspace(activearmature, selectedbones, constraint, targetspace, ownerspace)
        except:
            self.report({'ERROR'}, f"NO TARGET OBJECT SELECTED IN CONSTRAINT - OPERATION ABOARTED")
        return {'FINISHED'}



        


    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool=scene.my_tool
        enum = mytool.ExistingBoneConstraints_enum
        layout.prop(mytool, "ExistingBoneConstraints_enum")
        layout.prop(mytool, "targetspace_enum")
        layout.prop(self, "ownerspace_enum")
        
class VonPanel_RiggingTools__Submenu_ColorizeRig(bpy.types.Operator):
    bl_idname = "von.colorizerig"
    bl_label = "Colorize Rig"
    def execute(self, context):
        von_buttoncontrols.colorizerig(context)
        return {'FINISHED'}
    def invoke(self, context, event):   
        return context.window_manager.invoke_props_dialog(self)

#Creating Dropdown Menu Popup
class Von_Dropdown_AddCustomBoneshape(bpy.types.Operator):
    bl_label = "Add Custom Bone"
    bl_idname = "von.addcustomboneshape"

    temp_items = von_buttoncontrols.getexistingfilesindirectories(getfolderloc())
    temp_total = 0
    sendtoenum = []
    for i in temp_items:
            temp_total = temp_total + 1
            temp_total_string = f"'{str(temp_total)}'"
            #idescription = f"Click To Create {i} As An Avalible Boneshape"
            listofstrings = tuple((temp_total_string, os.path.splitext(os.path.basename(i))[0], i))
            sendtoenum.append(listofstrings)

    filetoloadselection_enum : EnumProperty(
        name = "FileSelectionToLoad",
        description = "Select An Option",   
        items = sendtoenum,
    )     # type: ignore
    
    shouldskeletonise_bool : BoolProperty(
        name="ShouldMeshBeSkeletonised",
        description="Tick the bool if you want the mesh to be loaded as a wireframe boneshape rather than a solid boneshape",
        default = False
        ) # type: ignore

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "filetoloadselection_enum")
        layout.prop(self, "shouldskeletonise_bool")
    
    def execute(self, context):
        temp_activebone =  bpy.context.active_pose_bone.name
        temp_activearmature = bpy.context.selected_objects[0].name
        temp_items = von_buttoncontrols.getexistingfilesindirectories(getfolderloc())

        von_createcontrols.spaceconsole(20)
        enumint = int(re.sub('\D', '', self.filetoloadselection_enum))
        enumint = enumint - 1
        objectname = os.path.splitext(os.path.basename(temp_items[enumint]))[0]
        von_createcontrols.create_mesh_from_json_data(self.shouldskeletonise_bool,objectname)
        controltouse = von_createcontrols.setname(von_createcontrols.load_data(objectname),self.shouldskeletonise_bool)
        bpy.context.view_layer.objects.active = bpy.data.objects[temp_activearmature]
        bpy.ops.object.mode_set(mode = 'POSE')
        von_buttoncontrols.searchforbone(temp_activearmature,temp_activebone)
        bpy.context.active_pose_bone.custom_shape = bpy.data.objects[str(controltouse)]
        return {'FINISHED'}    

class Von_Popout_SaveBoneNameToDict(bpy.types.Operator):
    bl_idname = "von.vrcsavebonenametodict"
    bl_label = "Save Bone Name To Dict"
    bl_description = "Add the selected bone's name to a library of your choice so that the MERGE ARMATURES button can identify these bones in future"
    def execute(self,context):
        scene = context.scene
        mytool=scene.my_tool
        obj = bpy.context.object
        
        if obj and obj.type == 'ARMATURE':
            followthrough = False
            if obj.mode != 'POSE':
                self.report({'ERROR'}, 'Must be in pose mode')
                return{'CANCELLED'}
            for i in bpy.context.selected_pose_bones:

                string_to_add = i
                string_to_add = string_to_add.name.lower()
                string_to_add = von_buttoncontrols.splitstringfromadditionalbones(string_to_add)

                directory_path = von_vrctools.get_directory() + "/Libraries/BoneNames"
                parentenumoption = mytool.jsondictionaryoptions_enum
                directory_path = os.path.join(directory_path, parentenumoption)
                key = mytool.jsondictionarykeyoptions_enum

                with open(directory_path, 'r') as file:
                    data = json.load(file)

                enum_items = []
                if key in data:
                    if isinstance(data[key], list):
                        # Check if the string is already in the list
                        if string_to_add not in data[key]:
                            data[key].append(string_to_add)  # Append the new string if not already present
                with open(directory_path, 'w') as file:
                    json.dump(data, file, indent=4)
            return{'FINISHED'}
    
        else:
            self.report({'WARNING'}, "Ensure An Armature Is Selected")
            return{'CANCELLED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool=scene.my_tool
        layout.prop(mytool, "jsondictionaryoptions_enum")
        layout.prop(mytool, "jsondictionarykeyoptions_enum")


class Von_InitializeArmaturesOperator(bpy.types.Operator):
    """Operator to initialize armatures and register dynamic properties."""
    bl_idname = "von.initialize_armatures"
    bl_label = "Initialize Armatures"
    bl_description = "Merge 2 or more selected armatures, the active armature will be the target that all additional bones, armature scales, and meshes will be focused on."

    def invoke(self, context, event):
        scene = bpy.context.scene
        my_tool = scene.my_tool
        # Retrieve the dynamic dictionary of options
        options = updatebonestandarizationoptions(self, context)
        if options:
            my_tool.set_vrc_tool_options(options)
            for option, values in options.items():
                prop_name = option.lower().replace(' ', '_') + "_choice"
                if not hasattr(my_tool, prop_name): 
                    enum_items = [(choice, choice, "") for choice in values]
                    setattr(
                        type(my_tool),
                        prop_name,
                        bpy.props.EnumProperty(items=enum_items, name=option),
                    )

        context.area.tag_redraw()
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool
        if hasattr(my_tool, 'vrc_tool_options'):
            options = my_tool.get_vrc_tool_options()
            if options:
                for option in options.keys():
                    prop_name = option.lower().replace(' ', '_') + "_choice"
                    if hasattr(my_tool, prop_name):
                        layout.prop(my_tool, prop_name)  # Display the EnumProperty for this key
                else:
                    layout.label(text="No options available.")
            else:
                layout.label(text="No options available.")


    def execute(self, context):
        selectedobjects = bpy.context.selected_objects
        tmp_selectedarmatures = []


        # Check armatures are selected
        for object in selectedobjects:
            if object.type == 'ARMATURE':
                tmp_selectedarmatures.extend(object.name)
        if len(tmp_selectedarmatures) == 0:
            reporterror(self, "Nothing Seleted")
            return{'FINISHED'}
        
        scene = bpy.context.scene
        my_tool = scene.my_tool
        selected_armatures = getselectedarmatures(context)
        targetdict = my_tool.AvalibleNamingConventions
        duplicatematches, undetectedbones, bonestorename = von_vrctools.filterbonesbyjsondictlist(selected_armatures,targetdict, self, False)

        #Standardizing Bone Names Between Armatures For Easier Modification Later On
        if hasattr(my_tool, 'vrc_tool_options'):
            options = my_tool.get_vrc_tool_options()
            if options:
                seldic = {}
                for option in options.keys():
                    opt_dict = {}
                    prop_name = option.lower().replace(' ', '_') + "_choice"
                    if hasattr(my_tool, prop_name):
                        selected_value = getattr(my_tool, prop_name)
                        opt_dict[option] = selected_value
                        von_vrctools.rename_bones_from_dict(selected_armatures, opt_dict, self  )

        bpy.ops.object.mode_set(mode='OBJECT')

        active_object = selectedobjects[0]
        #active_object = bpy.context.active_object
        target_armature = None
        source_armatures = []
        
        #set up the armature to add things to and where to get them from
        if active_object and active_object.type == 'ARMATURE':
            target_armature = active_object
        if target_armature:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE' and obj != target_armature.name:
                    source_armatures.append(obj)

        if target_armature:
            addto_detectedbones = []
            addto_undetectedbones = []
            addto_mergedbones = []
            #Generating the bones
            try:
                print("Checkpoint 1")
                von_vrctools.setrelativescalemod(selected_armatures, target_armature, self)
                createdbones = von_vrctools.generateextrabone(source_armatures, target_armature, self)
                von_vrctools.moveskeletalmesh(selected_armatures, target_armature,self)
                target_armature_bones = target_armature.data.bones
                #settings the colour of the target armature's bones
                for bone in createdbones:
                    if bone in target_armature_bones:
                        bpy.context.view_layer.objects.active = target_armature
                        bpy.context.object.data.bones[bone].color.palette = "THEME09"
                        addto_mergedbones.append(bone)
                    else:
                        self.report({'WARNING'}, f"Bone '{bone}' not found in armature")
                for bone in target_armature_bones:
                    if bone.name not in createdbones:
                        bpy.context.view_layer.objects.active = target_armature
                        bpy.context.object.data.bones[str(bone.name)].color.palette = "THEME03"
                        addto_detectedbones.append(str(bone.name))
            except Exception as e:
                reporterror(self, e)


        #Undetected bones
        if target_armature:
            print(target_armature)
            bpy.context.view_layer.objects.active = target_armature
            armaturebones = target_armature.data.bones
            print("Checkpoint 2")
            for bone in armaturebones:
                if bone in undetectedbones:
                    print(bone)
                    bpy.context.object.data.bones[bone].color.palette = "THEME01"
                    addto_undetectedbones.append(bone)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        target_armature.select_set(True)
        bpy.context.view_layer.objects.active = target_armature

        return {'FINISHED'}


        


class Von_SetNamingConventionsOperator(bpy.types.Operator):
    """Operator to initialize armatures and register dynamic properties."""
    bl_idname = "von.setnamingconvention"
    bl_label = "Set Naming Convention"
    bl_description = "Sets the naming convention of the selected armatures to the one desired."

    def execute(self,context):
        scene = bpy.context.scene
        my_tool = scene.my_tool
        selected_armatures = getselectedarmatures(context)
        targetdict = my_tool.AvalibleNamingConventions
        von_vrctools.filterbonesbyjsondictlist(selected_armatures, targetdict, self, False)
        return{'FINISHED'}



# ------------------------------------------------------------------------
#    Button Setup
# ------------------------------------------------------------------------

class VonPanel_RiggingTools__Submenu_CreateControl(bpy.types.Operator):
    bl_idname = "von.loadcustomcontrol"
    bl_label = "Load Custom Control"
    
    text : bpy.props.StringProperty(
        name="Enter Text", 
        default=""
        ) # type: ignore


    def execute(self, context):
        text = self.text
        von_createcontrols.create_mesh_from_json_data(False,text)
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class VonPanel_RiggingTools__Button_SaveNewControl(bpy.types.Operator):
    bl_idname = "von.savenewcontrol"
    bl_label = "Save Control"
    
    def execute(self, context):
        von_createcontrols.saveselectedmesh()
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class VonPanel_RiggingTools__WeightHammer(bpy.types.Operator):
    bl_idname = "von.weighthammer"
    bl_label = "Weight Hammer"
    
    def execute(self, context):
        von_createcontrols.averagevertexweights()
        return {'FINISHED'}

class VonPanel_RiggingTools__ClearVertexWeights(bpy.types.Operator):
    bl_idname = "von.clearvertexweights"
    bl_label = "Clear Vertex Weights"

    def execute(self, context):
        von_createcontrols.clear_vertex_weights()
        return {'FINISHED'}

class VonPanel_VRCTools__SelectDesiredName():
    bl_idname = "von.selectdesiredname"
    bl_label = "Select Desired Name"
class VonPanel_StressTestSkinning(bpy.types.Operator):
    bl_idname = "von.stresstestskinning"
    bl_label = "Test Skinning"

    testaxis: bpy.props.StringProperty(
        name="Primary Bone Axis",
        description="Choose which axis the bones are intended to rotate around",
        default="x"
    ) # type: ignore
    
    def execute(self, context):
        testaxis = self.testaxis
        selected_armatures = getselectedarmatures(context)
        von_optimisetools.stresstestrig(selected_armatures,testaxis)
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
class VonPanel_RigChecker_SkeletalMeshCheck(bpy.types.Operator):
    bl_idname = "von.rigchecker_skeletalmeshcheck"
    bl_label = "Skeletal Mesh Check"

    def execute(self, context):
        issues = defaultdict(lambda: defaultdict(set))
        selectedarmatures = getselectedarmatures(context)
        
        for armature in selectedarmatures:
            skeletalmeshes = get_meshes_using_armature(armature)
            issues = von_optimisetools.findemptyvertexgroups(skeletalmeshes,issues)
            issues = von_optimisetools.find_unweighted_vertices(skeletalmeshes, issues)
            issues = von_optimisetools.find_non_deform_weighted_bones(skeletalmeshes, issues)
            issues = von_optimisetools.check_multiple_armatures(skeletalmeshes, issues)
            issues = von_optimisetools.check_blender_suffix_bone_names(skeletalmeshes, issues)

        
        def draw(self, context):
            if issues:
                for rig_name, issue in issues.items():
                    self.layout.label(text=f"{rig_name}")
                    for issue_type, bones in issue.items():
                        for bone in bones:
                            self.layout.label(text=f"  {issue_type}: {bone}")
            else:
                self.layout.label(text=f"No Rig Issues Detected")
        context.window_manager.popup_menu(draw, title="Rig Check Results", icon='INFO')



        return {'FINISHED'}

class VonPanel_RigChecker_ArmatureCheck(bpy.types.Operator):
    bl_idname = "von.rigchecker_armaturecheck"
    bl_label = "Armature Check"

    tolerance: bpy.props.FloatProperty(
        name="Minimum Bone Size",
        description="Minimum Acceptable Size Of Bone",
        default=0.1
    ) # type: ignore

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        scene = context.scene
        my_tool = scene.my_tool
        issues = defaultdict(lambda: defaultdict(set))
        selectedarmatures = getselectedarmatures(context)
        definedroot = my_tool.definedroot
        posebonelimit = my_tool.posebonelimit
        tolerance = self.tolerance
        issues = von_optimisetools.checkbones(selectedarmatures, issues, definedroot, posebonelimit)
        issues = von_optimisetools.checkconstraints(selectedarmatures, issues)
        issues = von_optimisetools.check_zero_length_bones(selectedarmatures, issues, tolerance)
        def draw(self, context):
            layout = self.layout
            if issues:
                spaceconsole(5)
                row = layout.row()
                split = row.split(factor=0.3)
                col_left = split.column()
                col_right = split.column()
                for rig_name, issue in issues.items():
                    col_left.separator()
                    col_left.label(text=f"{rig_name}")
                    col_right.label(text=f"")

                    for issue_type, bones in issue.items():                        
                        col_left.label(text=issue_type)
                        for bone in bones:
                            col_right.label(text=bone)
                spaceconsole(5)
            else:
                    layout.label(text="No Rig Issues Detected")
        context.window_manager.popup_menu(draw, title="Rig Check Results", icon='INFO')
        return {'FINISHED'}


class VonPanel_RigChecker_CheckBones(bpy.types.Operator):
    bl_idname = "von.rigchecker_checkbones"
    bl_label = "Bones"

    def execute(self, context):
        scene = bpy.context.scene
        my_tool = scene.my_tool
        issues = defaultdict(lambda: defaultdict(set))
        selectedarmatures = getselectedarmatures(context)

        definedroot = my_tool.definedroot
        posebonelimit = my_tool.posebonelimit

        issues = von_optimisetools.checkbones(selectedarmatures, issues, definedroot, posebonelimit)
        
        
        def draw(self, context):
            if issues:
                for rig_name, issue in issues.items():
                    self.layout.label(text=f"{rig_name}")
                    for issue_type, bones in issue.items():
                        for bone in bones:
                            self.layout.label(text=f"  {issue_type}: {bone}")
            else:
                self.layout.label(text=f"No Rig Issues Detected")
        context.window_manager.popup_menu(draw, title="Rig Check Results", icon='INFO')
        return {'FINISHED'}

class VonPanel_RigChecker_CheckConstraints(bpy.types.Operator):
    bl_idname = "von.rigchecker_checkconstraints"
    bl_label = "Constraints"

    def execute(self, context):
        scene = bpy.context.scene
        my_tool = scene.my_tool
        issues = defaultdict(lambda: defaultdict(set))
        selectedarmatures = getselectedarmatures(context)
        issues = von_optimisetools.checkconstraints(selectedarmatures, issues)

        
        
        def draw(self, context):
            if issues:
                for rig_name, issue in issues.items():
                    self.layout.label(text=f"{rig_name}")
                    for issue_type, bones in issue.items():
                        for bone in bones:
                            self.layout.label(text=f"  {issue_type}: {bone}")
            else:
                self.layout.label(text=f"No Rig Issues Detected")
        context.window_manager.popup_menu(draw, title="Rig Check Results", icon='INFO')
        return {'FINISHED'}

class VonPanel_QuickFixes_CullOrphans(bpy.types.Operator):
    bl_idname = "von.cullorphans"
    bl_label = "Cull Orphans"

    def execute(self, context):
        scene = bpy.context.scene
        my_tool = scene.my_tool

        selectedarmatures = getselectedarmatures(context)
        definedroot = my_tool.definedroot

        von_optimisetools.cullorphans(selectedarmatures, definedroot)


# ------------------------------------------------------------------------
#    Menu Setup
# ------------------------------------------------------------------------

class VonPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonTools'
    bl_options = {"DEFAULT_CLOSED"}

class VONPANEL_PT_primary_panel(VonPanel, bpy.types.Panel):
    bl_idname = "VONTOOLS_PT_primary_panel"
    bl_label= "Von Tools"

    def draw(self,context):
        layout = self.layout
        layout.label(text= "Vontools For All Your Rigging Needs")

class VONPANEL_PT_rigging_tools(VonPanel, bpy.types.Panel):
    bl_parent_id = "VONTOOLS_PT_primary_panel"
    bl_label = "Rigging Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("von.popoutpanelbonesearch")
        row = layout.row()
        row.operator("von.addcustomboneshape")
        row.operator("von.savenewcontrol")
        layout.operator("von.masssetboneconstraintspace")
        layout.operator("von.colorizerig")

class VONPANEL_PT_skinning_tools(VonPanel, bpy.types.Panel):
    bl_parent_id = "VONTOOLS_PT_primary_panel"
    bl_label = "Skinning Tools"

    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool


        box = layout.box()
        box.label(text="Vertex Weight Tools")
        row = box.row()
        row.operator("von.weighthammer")
        row.operator("von.clearvertexweights")

        box = layout.box()
        row = box.row
        box.label(text="Armature Verification")
        box.prop(my_tool, "definedroot")
        box.prop(my_tool, "posebonelimit")
        row = box.row()
        row.operator("von.rigchecker_checkbones")
        row.operator("von.rigchecker_checkconstraints")
        box.operator("von.rigchecker_armaturecheck")
        box.operator("von.rigchecker_skeletalmeshcheck")

        layout.menu("_MT_quickfix_tools_MT_", text="Quick Fixes")

class VONPANEL_PT_skinning_tools_quickfixes(bpy.types.Menu):
    bl_idname = "_MT_quickfix_tools_MT_"
    bl_label = "_MT_Quickfix Tools_MT_"
    

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        layout.label(text="Quickfix Tools")
        layout.operator("von.cullorphans")
        obj = bpy.context.active_object
        if obj and obj.type == 'MESH':
            op = layout.operator("object.vertex_group_clean", text="Clean Vertex Groups")
            op.limit = 0.2



class VONPANEL_PT_armaturemerge(VonPanel, bpy.types.Panel):
    bl_parent_id = "VONTOOLS_PT_primary_panel"
    bl_label = "Armature Merge Tools"

    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool
        row = layout.row()
        scene = context.scene
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.prop(my_tool, "stringspacerreplacer")
        layout.operator("von.vrcsavebonenametodict")
        layout.prop(my_tool, "AvalibleNamingConventions")
        row = layout.row()
        row.operator("von.initialize_armatures", text="Merge Armatures")
        row.operator("von.setnamingconvention", text="Set Naming Convention")
        

classes = (
    MySettings,
    VONPANEL_PT_primary_panel,
    VONPANEL_PT_rigging_tools,
    VONPANEL_PT_skinning_tools,
    VonPanel_RiggingTools__Submenu_BoneSearch,
    VonPanel_RiggingTools__Submenu_CreateControl,
    VonPanel_RiggingTools__Button_SaveNewControl,
    Von_Dropdown_AddCustomBoneshape,
    Von_Popout_SaveBoneNameToDict,
    Von_InitializeArmaturesOperator,
    VONPANEL_PT_armaturemerge,
    VonPanel_RiggingTools_Submenu_MassSetBoneConstraintSpace,
    VonPanel_RiggingTools__Submenu_ColorizeRig,
    VonPanel_RiggingTools__WeightHammer,
    VonPanel_RiggingTools__ClearVertexWeights,
    VonPanel_RigChecker_ArmatureCheck,
    Von_SetNamingConventionsOperator,
    VonPanel_StressTestSkinning,
    VonPanel_RigChecker_CheckBones,
    VonPanel_RigChecker_CheckConstraints,
    VonPanel_RigChecker_SkeletalMeshCheck,
    VONPANEL_PT_skinning_tools_quickfixes,
    VonPanel_QuickFixes_CullOrphans,
    )


def von_menupopup_register():
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)




def von_menupopup_unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool