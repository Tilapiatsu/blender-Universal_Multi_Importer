import re
import bpy

def get_bversion():
    '''
    Returns the current blender version
    '''
    bversion_string = bpy.app.version_string
    bversion_reg = re.match(r"^(\d?\d)[.](\d?\d)[.](\d?\d)", bversion_string)
    return float(bversion_reg.group(1)) + float(bversion_reg.group(2)) * 0.1 + float(bversion_reg.group(3)) * 0.001

BVERSION = get_bversion()
