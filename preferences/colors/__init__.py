from . import presets
from . import colors

def register():
    presets.register()
    colors.register()


def unregister():
    colors.unregister()
    presets.unregister()