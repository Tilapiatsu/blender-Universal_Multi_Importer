from . import blend_format

modules = (blend_format, )

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()