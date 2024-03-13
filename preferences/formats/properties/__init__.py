from . import properties
from .properties import PG_Operator, PG_ImportSettings, PG_UMISettings, update_file_stats, update_file_extension_selection

def register():
    properties.register()


def unregister():
    properties.unregister()