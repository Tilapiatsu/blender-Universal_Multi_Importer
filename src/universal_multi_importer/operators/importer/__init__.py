from . import OP_import
from . import ui

modules = (ui, OP_import)


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
