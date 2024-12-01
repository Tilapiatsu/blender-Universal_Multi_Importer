import re
import bpy

def get_bversion():
    '''
    Returns the current blender version
    '''
    bversion_string = bpy.app.version_string
    bversion_reg = re.match("^(\d\.\d?\d)", bversion_string)
    return float(bversion_reg.group(0))

BVERSION = get_bversion()
