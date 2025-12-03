import bpy # type: ignore
from bpy.types import PropertyGroup # type: ignore

class common_data(PropertyGroup):
    ExistingBoneConstraints_enum : bpy.props.EnumProperty(
        name = "",
        description = "",
        items = getselectedbonesforenum, # type: ignore
        update = updateexistingboneconstraintsenum # type: ignore
    ) # type: ignore