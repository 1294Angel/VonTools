import bpy # type: ignore

def spaceconsole(temp):
    xx = temp
    while xx > 0:
        xx = xx -1
        print("")

def reporterror(self, e):
    self.report({'ERROR'}, f"Unexpected Error: {str(e)}")

def getselectedarmatures(context):
    return [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
    """I've been using this version, but checking selected objects seems more efficient
    [obj for obj in bpy.data.objects if obj.type == 'ARMATURE' and obj.select_get()]"""

