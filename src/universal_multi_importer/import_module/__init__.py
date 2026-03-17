from . import blend_format, import_as_geometry_node, import_reference

modules = (blend_format, import_as_geometry_node, import_reference)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
