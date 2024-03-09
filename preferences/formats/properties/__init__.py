from . import properties
from .properties import PG_Operator, PG_ImportSettings, PG_UMISettings, update_file_stats

def register():
    properties.register()


def unregister():
    properties.unregister()