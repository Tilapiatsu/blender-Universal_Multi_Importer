from . import format_preset, import_preset

def register():
    format_preset.register()
    import_preset.register()

def unregister():
    import_preset.unregister()
    format_preset.unregister()