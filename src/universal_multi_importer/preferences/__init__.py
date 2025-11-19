import bpy
from .. import ADDON_PACKAGE


from . import formats
from . import preferences
from . import colors
from . import operators

modules = (formats, colors, preferences, operators)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()