from . import presets
from . import colors

modules = (presets, colors)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()