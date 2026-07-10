from . import importer

modules = (importer,)

try:
    from . import batcher

    modules = modules + (batcher,)
except ImportError:
    pass


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
