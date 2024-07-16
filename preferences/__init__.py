import bpy
from .. import ADDON_PACKAGE


from . import formats
from . import preferences
from . import colors
from . import operators

def register():
    formats.register()
    colors.register()
    preferences.register()
    operators.register()


def unregister():
    operators.unregister()
    preferences.unregister()
    colors.unregister()
    formats.unregister()