from . import ui, OP_command_batcher

modules = (ui, OP_command_batcher)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
