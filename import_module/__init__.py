from . import blend_format, import_as_geometry_node

modules = (blend_format, import_as_geometry_node)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()