from . import OP_UL_operators, OP_UL_preset

modules = (OP_UL_operators, OP_UL_preset)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
