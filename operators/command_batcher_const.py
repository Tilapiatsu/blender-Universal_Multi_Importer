import bpy
from mathutils import Vector
import time

COMMAND_BATCHER_INPUT_ITEMS = [ ('ITEM_INDEX', 'Item Index (int)', ''),
                                ('ITEM_NAME', 'Item Name (str)', ''),
                                ('ITEM_DATA', 'Item Data (str)', ''),
                                ('OBJECT_BBOX', 'Object Bounding Box Size (vector3)', ''),
                                ('TIMEF', 'Time (float)', ''),
                                ('TIMESTR', 'Time (string)', ''),
                                ('BVERSION', 'Blender Version (float)', '')]

COMMAND_BATCHER_INPUT_STRING = [ n[0] for n in COMMAND_BATCHER_INPUT_ITEMS]

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
    return [str(item_index),
            item_name,
            str(item_data),
            str((0, 0, 0)) if object is None else vector_to_string(get_bound_box_size(object)),
            str(time.time()),
            time.asctime(),
            bpy.app.version_string]

