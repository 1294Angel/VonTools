# ------------------------------------------------------------------------
#    Addon Info
# ------------------------------------------------------------------------


import bpy, sys, os, re # type: ignore
from bpy.types import Operator # type: ignore
from bpy_extras.object_utils import AddObjectHelper # type: ignore
from bpy.types import Operator # type: ignore
from bpy_extras.object_utils import object_data_add # type: ignore
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
    von_vrctools.ENUMUPDATE_gatherheirarchydata()

def updatetargetspaceenumlist(self, context):
    von_createcontrols.spaceconsole(5)
    print("UPDATING TARGET SPACE ENUMLIST")
    factor = von_buttoncontrols.checkboneconstrainttarget(von_buttoncontrols.getselectedbones(context))
    enumlist = []
    print(f"Factor - {factor}")

    if factor == None:
        return[("-1000", "NONEVALUE, REPORT ERROR")]
    if factor == "ARMATURE":
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description"), ("4", "POSE", "Description"), ("5", "LOCAL_WITH_PARENT", "Description"), ("6", "LOCAL_OWNER_ORIENT", "Description")]
        return enumlist
    if factor == "NOTARMATURE":
        enumlist = [("1", "LOCAL", "Description"), ("2", "WORLD", "Description"), ("3", "CUSTOM", "Description")]
        return enumlist
    

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    my_bool : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        ) # type: ignore

    my_int : IntProperty(
        name = "Set a value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        ) # type: ignore

    my_float : FloatProperty(
        name = "Set a value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        ) # type: ignore
        
    bonebeingsearched: StringProperty(
        name="String",
        description="",
        default="",
        maxlen=1024,
        ) # type: ignore

    my_enum: EnumProperty(
        name = "",
        description = "",   
        items = [],
    ) # type: ignore

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

    jsondictionaryoptions_enum : bpy.props.EnumProperty(
        name = "Json Dict Options - ",
        description = "The Possible Json Dictionaries Edit",
        items = updateexistingjsondictonaries,
        update = updateexistingjsondictonaries
    ) # type: ignore

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

        von_buttoncontrols.setboneconstraintspace(activearmature, selectedbones, constraint, targetspace, ownerspace)

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

    def execute(self,context):
        print("EXECUTING ADD TO DICTIONARY")
        return{'FINISHED'}
    def invoke(self, context, event):
        wm = context.window_manager
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool=scene.my_tool
        layout.prop(mytool, "jsondictionaryoptions_enum")


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



# ------------------------------------------------------------------------
#    Menu Setup
# ------------------------------------------------------------------------

class VonPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VonTools'
    bl_options = {"DEFAULT_CLOSED"}

class VONPANEL_PT_PrimaryPanel(VonPanel, bpy.types.Panel):
    bl_idname = "von.vontools"
    bl_label= "Von Tools"

    def draw(self,context):
        layout = self.layout
        layout.label(text= "Vontools For All Your Rigging Needs")

class VONPANEL_PT_RiggingTools(VonPanel, bpy.types.Panel):
    bl_parent_id = "von.vontools"
    bl_label = "Rigging Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene
        mytool=scene.my_tool

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
    bl_parent_id = "von.vontools"
    bl_label = "VRChat Tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        scene = context.scene

        row.label(text= "VRChat Tools", icon= 'CUBE')
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("von.vrcsavebonenametodict")


classes = (
    MySettings,
    VONPANEL_PT_PrimaryPanel,
    VONPANEL_PT_RiggingTools,
    VonPanel_RiggingTools__Submenu_BoneSearch,
    VonPanel_RiggingTools__Submenu_CreateControl,
    VonPanel_RiggingTools__Button_SaveNewControl,
    Von_Dropdown_AddCustomBoneshape,
    Von_Popout_SaveBoneNameToDict,
    VONPANEL_PT_VRCTools,
    VonPanel_RiggingTools_Submenu_MassSetBoneConstraintSpace,
    VonPanel_RiggingTools__Submenu_ColorizeRig,
    VonPanel_RiggingTools__WeightHammer,
    VonPanel_RiggingTools__ClearVertexWeights
)

def von_menupopup_register():
    print(f'Menu File Initiated')
    from bpy.utils import register_class # type: ignore
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)



def von_menupopup_unregister():
    from bpy.utils import unregister_class # type: ignore
    for cls in reversed(classes):
        unregister_class(cls)

    del bpy.types.Scene.my_tool