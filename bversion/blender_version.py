from bpy.app import version as blender_version
from .version import Version

def get_bversion():
    '''
    Returns the current blender version
    '''

    version = Version(blender_version)
    return version

BVERSION = get_bversion()
