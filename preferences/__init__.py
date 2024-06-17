import bpy
from .. import ADDON_PACKAGE


from . import formats
from . import preferences
from . import colors

def register():
    formats.register()
    colors.register()
    preferences.register()


def unregister():
    preferences.unregister()
    colors.unregister()
    formats.unregister()