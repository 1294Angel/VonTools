
# ------------------------------------------------------------------------
#    Addon Info
# ------------------------------------------------------------------------


import bpy, sys, os, re, json # type: ignore
from bpy_extras.object_utils import (AddObjectHelper, object_data_add) # type: ignore
from mathutils import Vector # type: ignore
from math import radians # type: ignore
from pathlib import Path
from bpy.props import (StringProperty, # type: ignore
                       BoolProperty,
                       IntProperty,
                       FloatProperty, 
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel, # type: ignore
                       Menu,
                       Operator,
                       PropertyGroup,
                       )
from . import von_buttoncontrols
from . import von_createcontrols
from . import von_vrctools

# ------------------------------------------------------------------------
#    Dynamic Enum Population
# ------------------------------------------------------------------------
def updateexistingboneconstraintsenum(self, context):
    von_buttoncontrols.getselectedbonesforenum(self, context)

def updateexistingjsondictonaries(self, context):
    #FUNCTIONAL
    return von_vrctools.ENUMUPDATE_gatherheirarchydata(self)
def updatejsonkeyoptions(self, context):

    directory_path = von_vrctools.get_directory() + "/Libraries/BoneNames"
    parentenumoption = self.jsondictionaryoptions_enum
    directory_path = os.path.join(directory_path, parentenumoption)

    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The file {directory_path} does not exist.")
    
    with open(directory_path, 'r') as file:
        data = json.load(file)

    iterations = -1
    enum_items = []
    for key in data.keys():
        iterations = iterations + 1
        enum_items.append((key, key, f"Description for {key}"))

    return enum_items

def updatebonestandarizationoptions(self, context):
    print("")
    print("UPDATE BONE STANDARDIZATION OPTIONS _ ENUM")
    my_tool = context.scene.my_tool
    selected_dict = my_tool.AvalibleNamingConventions
    targetdict = von_vrctools.gatherspecificjsondictkeys(selected_dict)
    all_matches = {}
    selected_armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]
    all_matches = von_vrctools.filterbonesbyjsondictlist(selected_armatures, von_vrctools.gatherjsondictkeys(self, targetdict), targetdict, self, True)
    
    return all_matches


def updatebonestandarizationoptions_enum(self, context, key):
    print("")
    print("UPDATE BONE STANDARDIZATION OPTIONS _ ENUM")
    my_tool = context.scene.my_tool
    selected_dict = my_tool.AvalibleNamingConventions
    targetdict = von_vrctools.gatherspecificjsondictkeys(selected_dict)
    all_matches = {}
    selected_armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]
    all_matches = von_vrctools.filterbonesbyjsondictlist(selected_armatures, von_vrctools.gatherjsondictkeys(self, targetdict), targetdict, self, True)
    
    enum_items = []
    if key in all_matches:
        values = all_matches[key]
        enum_items = [(choice, choice, "") for choice in values] 
    print(f"TargetDict = {selected_dict}")
    print(f"Enum items = {enum_items}")
    return enum_items

def updatetargetspaceenumlist(self, context):
    print("RUNNING UPDATETARGETSPACE??")
    von_createcontrols.spaceconsole(5)
    factor = von_buttoncontrols.checkboneconstrainttarget(von_buttoncontrols.getselectedbones(context))
    enumlist = []
    print("Factor =")
    print(factor)
    if factor == "ARMATURE":
        print("FACTOR ARMATURE")
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description"), ("4", "POSE", "Description"), ("5", "LOCAL_WITH_PARENT", "Description"), ("6", "LOCAL_OWNER_ORIENT", "Description")]
        return enumlist
    if factor != "ARMATURE":
        print("FACTOR NOTARMATURE")
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description")]
        return enumlist        

def updateavaliblenamingconventions(self,context):
    namingconventions = ([])
    directory_path = von_vrctools.get_directory() + "/Libraries/BoneNames"
    for filename in os.listdir(directory_path):
        filename = str(filename)
        namingconventions.append((filename,filename,"This is a fileame"))
    print(f"Naming Conventions {namingconventions}")
    return namingconventions

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MySettings(bpy.types.PropertyGroup):
#--------------
  
    ExistingBoneConstraints_enum : bpy.props.EnumProperty(
        name = "",
        description = "",
        items = von_buttoncontrols.getselectedbonesforenum,
        update = updateexistingboneconstraintsenum
    ) # type: ignore

    targetspace_enum: EnumProperty(
        name = "Target Space - ",
        description = "The Setting Target Space will be set to",   
        items = updatetargetspaceenumlist,
        update = updatetargetspaceenumlist
    ) # type: ignore
#--------------
    jsondictionaryoptions_enum : bpy.props.EnumProperty(
        name = "Avalible Json Dictionaries - ",
        description = "Choose an option",
        items = updateexistingjsondictonaries,
        update = lambda self, context: context.scene.my_settings.option_enum.update(context)
    ) # type: ignore
    
    jsondictionarykeyoptions_enum: bpy.props.EnumProperty(
        name="Avalible Keys - ",
        description="Choose an option",
        items=updatejsonkeyoptions
    ) # type: ignore

    vrc_tool_options: bpy.props.StringProperty(
        name="TempName",
        description="Store serialized dictionary as a JSON string",
        default="{}"
    ) # type: ignore


#--------------
    AvalibleNamingConventions: bpy.props.EnumProperty(
        name = "AvalibleNamingConventions",
        description = "Choose an option from the list to standardize naming conventions",
        items = updateavaliblenamingconventions,
    ) # type: ignore
#--------------

    def get_vrc_tool_options(self):
        """Deserialize the JSON string into a dictionary."""
        return json.loads(self.vrc_tool_options)
    
    def set_vrc_tool_options(self, value):
        """Serialize a dictionary into a JSON string."""
        self.vrc_tool_options = json.dumps(value)
#--------------
    pass



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

    temp_items = von_buttoncontrols.getexistingfilesindirectories(von_createcontrols.getfolderloc())
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
        temp_items = von_buttoncontrols.getexistingfilesindirectories(von_createcontrols.getfolderloc())

        von_createcontrols.spaceconsole(20)
        enumint = int(re.sub('\D', '', self.filetoloadselection_enum))
        enumint = enumint - 1
        objectname = os.path.splitext(os.path.basename(temp_items[enumint]))[0]
        von_createcontrols.create_mesh_from_json_data(self.shouldskeletonise_bool,objectname)
        controltouse = von_createcontrols.setname(von_createcontrols.load_data(objectname),self.shouldskeletonise_bool)
        bpy.context.view_layer.objects.active = bpy.data.objects[temp_activearmature]
        bpy.ops.object.mode_set(mode = 'POSE')
        von_buttoncontrols.searchforbone(temp_activearmature,temp_activebone)
        von_createcontrols.setcontrol(controltouse)






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

        options = updatebonestandarizationoptions(self, context)

        if options:
            my_tool.set_vrc_tool_options(options)
            for option, values in options.items():
                prop_name = option.lower().replace(' ', '_') + "_choice"
                if not hasattr(my_tool, prop_name):
                    setattr(
                        type(my_tool),
                        prop_name,
                        bpy.props.EnumProperty(
                            items=lambda self, context: updatebonestandarizationoptions_enum(self, context, option),
                            name=option
                        )
                    )
        context.area.tag_redraw()
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool

        layout.prop(my_tool, "AvalibleNamingConventions")
        layout.separator()

        if hasattr(my_tool, 'vrc_tool_options'):
            options = my_tool.get_vrc_tool_options()
            if options:
                for option in options.keys():
                    prop_name = option.lower().replace(' ', '_') + "_choice"
                    if hasattr(my_tool, prop_name):
                        layout.prop(my_tool, prop_name)
            else:
                layout.label(text="No options available.")
        else:
            layout.label(text="No options available.")

    def execute(self, context):
        scene = bpy.context.scene
        my_tool = scene.my_tool
        selected_armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]
        targetdict = my_tool.AvalibleNamingConventions
        duplicatematches, undetectedbones, bonestorename = von_vrctools.filterbonesbyjsondictlist(selected_armatures, von_vrctools.gatherjsondictkeys(self, targetdict),targetdict, self, False)
        initiallyselectedarmature = bpy.context.view_layer.objects.active

        #Standardizing Bone Names Between Armatures For Easier Modification Later On
        for armature in selected_armatures:
            bpy.context.view_layer.objects.active = armature
            armaturebones = armature.data.bones
            for bone in undetectedbones:
                if bone in armaturebones:
                    bpy.context.object.data.bones[bone].color.palette = "THEME01"
            bpy.context.view_layer.objects.active = initiallyselectedarmature
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

        active_object = bpy.context.selected_objects[0]
        #active_object = bpy.context.active_object
        target_armature = None
        source_armatures = []
        endswithnumbers = False
        
        if active_object and active_object.type == 'ARMATURE':
            target_armature = active_object
        if target_armature:
            for obj in bpy.context.selected_objects:
                if obj.type == 'ARMATURE' and obj != target_armature.name:
                    source_armatures.append(obj)

            # Debug output
            #print(f"Target Armature: {target_armature.name if target_armature else 'None'}")
            #print(f"Source Armatures: {[obj.name for obj in source_armatures]}")
        if target_armature:
            #Generating the bones
            von_vrctools.setrelativescalemod(selected_armatures, target_armature, self)
            createdbones = von_vrctools.generateextrabone(source_armatures, target_armature, self)
            von_vrctools.moveskeletalmesh(selected_armatures, target_armature,self)
            target_armature_bones = target_armature.data.bones
            for bone in createdbones:
                print(f"COLOURING - {bone}")
                bpy.context.object.data.bones[bone].color.palette = "THEME09"
            for bone in target_armature_bones:
                bone = bone.name
                if bone not in createdbones:
                    bpy.context.object.data.bones[bone].color.palette = "THEME15"






            

        return {'FINISHED'}
        

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
class VonPanel_TESTButton(bpy.types.Operator):
    bl_idname = "von.testbutton"
    bl_label = "Test Button"

    def execute(self, context):
        print("EXECUTING TEST BUTTON")
        selectedobjects = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]
        active_object = selectedobjects[0]
        selectedobjects.remove(selectedobjects[0])
        von_vrctools.setrelativescalemod(selectedobjects, active_object, self)
        return {'FINISHED'}



# ------------------------------------------------------------------------
#    Menu Setup
# ------------------------------------------------------------------------

class VonPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonTools'
    bl_options = {"DEFAULT_CLOSED"}

class VONPANEL_PT_primary_panel(VonPanel, bpy.types.Panel):
    bl_idname = "VONTOOLS_PT_my_panel"
    bl_label= "Von Tools"

    def draw(self,context):
        layout = self.layout
        layout.label(text= "Vontools For All Your Rigging Needs")

class VONPANEL_PT_rigging_tools(VonPanel, bpy.types.Panel):
    bl_parent_id = "VONTOOLS_PT_my_panel"
    bl_label = "Rigging Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene

        row.label(text= "Bone Manipulation", icon= 'CUBE')
        #Colorize Rig

        #Bone Search
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("von.popoutpanelbonesearch")
        

        row.label(text= "Bone Shapes", icon= 'CUBE')
        #create object
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("von.addcustomboneshape")
        layout.operator("von.savenewcontrol")
        layout.operator("von.masssetboneconstraintspace")
        layout.operator("von.colorizerig")

        layout.operator("von.weighthammer")
        layout.operator("von.clearvertexweights")


        row.label(text= "Weight Painting", icon= 'CUBE')

class VONPANEL_PT_VRCTools(VonPanel, bpy.types.Panel):
    bl_parent_id = "VONTOOLS_PT_my_panel"
    bl_label = "VRChat Tools"

    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool
        row = layout.row()
        scene = context.scene
        row.label(text= "VRChat Tools", icon= 'CUBE')
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("von.vrcsavebonenametodict")
        #layout.operator("von.testbutton", text = "Test Button!")
        layout.operator("von.initialize_armatures", text="Merge Armatures")

classes = (
    MySettings,
    VONPANEL_PT_primary_panel,
    VONPANEL_PT_rigging_tools,
    VonPanel_RiggingTools__Submenu_BoneSearch,
    VonPanel_RiggingTools__Submenu_CreateControl,
    VonPanel_RiggingTools__Button_SaveNewControl,
    Von_Dropdown_AddCustomBoneshape,
    Von_Popout_SaveBoneNameToDict,
    Von_InitializeArmaturesOperator,
    VONPANEL_PT_VRCTools,
    VonPanel_RiggingTools_Submenu_MassSetBoneConstraintSpace,
    VonPanel_RiggingTools__Submenu_ColorizeRig,
    VonPanel_RiggingTools__WeightHammer,
    VonPanel_RiggingTools__ClearVertexWeights,
    VonPanel_TESTButton
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