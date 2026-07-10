from . import log_file, check_addon_dependencies

modules = (log_file, check_addon_dependencies)

try:
    from . import extensions

    modules = modules + (extensions,)

except ImportError:
    pass


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
