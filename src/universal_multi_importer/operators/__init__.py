from . import OP_command_batcher, OP_import
from . import ui

modules = (ui, OP_command_batcher, OP_import)

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()