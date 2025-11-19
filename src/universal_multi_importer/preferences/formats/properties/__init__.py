from . import properties
from .properties import PG_Operator, PG_ImportSettings, PG_UMISettings, update_file_stats, update_file_extension_selection

modules = (properties, )

def register():
    for m in modules:
        m.register()

def unregister():
    for m in reversed(modules):
        m.unregister()
