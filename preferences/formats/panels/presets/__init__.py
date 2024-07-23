from . import format_preset, import_preset

modules = (format_preset, import_preset)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()
