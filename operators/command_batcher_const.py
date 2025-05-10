import bpy
from mathutils import Vector
import time
from ..umi_const import get_umi_settings

COMMAND_BATCHER_INPUT_ITEMS = [ ('ITEM_NAME', 'Item Name (str)', 'Returns the name of the item. The item depends on what is being processed : If the processed item is an object, it will returns the object name. If the processed item is a material, it will return the material name etc ...'),
                                ('ITEM_INDEX', 'Item Index (int)', 'Returns a integer from 0 to n where 0 is the first item processed and n the last item.'),
                                ('ITEM_DATA', 'Item Data (str)', r'Returns a string that point to the data of the currently processed item. If the processed item is an object, it will return bpy.data.objects[ObjectName],  and If the processed item is a material, it will return bpy.data.materials[MaterialName].\nIt allows you to access the data of the currently processed item and modify it the way you want'),
                                ('OBJECT_BBOX', 'Object Bounding Box Size (vector3)', 'Works if the processed item is an object : It returns a Vector3 that represent the bounding box size of the object.'),
                                ('TIMEF', 'Time (float)', 'Returns a float representing the current time'),
                                ('TIMESTR', 'Time (str)', 'Returns a string representing the curent date'),
                                ('BVERSION', 'Blender Version (float)', 'Returns a float representing the current blender version')]

COMMAND_BATCHER_INPUT_STRING = [ n[0] for n in COMMAND_BATCHER_INPUT_ITEMS]
COMMAND_BATCHER_ITEM_COUNT = len(COMMAND_BATCHER_INPUT_ITEMS)
COMMAND_BATCHER_VARIABLE_PREFIX = 'inject'

def revert_to_default(self, context):
    umi_settings = get_umi_settings()
    if umi_settings.umi_updating_batcher_variable:
        return

    umi_settings.umi_updating_batcher_variable = True
    for v in COMMAND_BATCHER_VARIABLE:
        exec(f"self.{v['property']} = {v['default']}", {'self':self})
    umi_settings.umi_updating_batcher_variable = False


def get_command_batcher_variable():
    variables = [{'default':f'"<{v[0]}>"', 'type':'STRING', 'property':f'{COMMAND_BATCHER_VARIABLE_PREFIX}_{v[0].lower()}', 'name':v[1], 'description':v[2], 'option':{'SKIP_SAVE'}, 'set':revert_to_default} for v in COMMAND_BATCHER_INPUT_ITEMS]
    return tuple(variables)

COMMAND_BATCHER_VARIABLE = get_command_batcher_variable()


def get_bound_box_size(obj) -> Vector:
    bound_box = obj.bound_box
    bbox_size = Vector((0, 0, 0))
    p_inf = float('inf')
    n_inf = float('-inf')
    bbox_min = Vector((p_inf, p_inf, p_inf))
    bbox_max = Vector((n_inf, n_inf, n_inf))
    for v in bound_box:
        bbox_min = Vector((min(bbox_min[0], v[0] * obj.scale[0]), min(bbox_min[1], v[1] * obj.scale[1]), min(bbox_min[2], v[2] * obj.scale[2])))
        bbox_max = Vector((max(bbox_max[0], v[0] * obj.scale[0]), max(bbox_max[1], v[1] * obj.scale[1]), max(bbox_max[2], v[2] * obj.scale[2])))

    bbox_size = Vector((abs(bbox_max[0] - bbox_min[0]), abs(bbox_max[1] - bbox_min[1]), abs(bbox_max[2] - bbox_min[2])))
    return bbox_size

def vector_to_string(v) -> str:
    s = str((v[0], v[1], v[2]))
    return s

def get_command_batcher_output_string(item_index: int, item_name:str, item_data:str, object=None) -> list[str]:
    return [item_name,
            str(item_index),
            str(item_data),
            str((0, 0, 0)) if object is None else vector_to_string(get_bound_box_size(object)),
            str(time.time()),
            time.asctime(),
            bpy.app.version_string]

