from . import OP_UL_operators, OP_UL_preset, OP_UL_file_selection

modules = (OP_UL_operators, OP_UL_preset, OP_UL_file_selection)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()